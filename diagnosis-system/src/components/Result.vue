<template>
  <el-row :gutter="20" class="container">
    <el-col :span="12" class="left-panel">
      <el-card class="result-card">
        <div class="control-group">
          <div class="model-selector">
            <label class="selector-label">模型选择：</label>
            <el-radio-group v-model="model" size="medium">
              <el-radio-button label="CNN" class="model-btn">CNN</el-radio-button>
              <el-radio-button label="MPINet" class="model-btn">MPINet</el-radio-button>
            </el-radio-group>
          </div>
          <el-button 
            type="primary" 
            size="medium" 
            @click="getFileContent"
            class="action-btn"
            :loading="loading">
            {{ loading ? '加载中...' : '查看训练结果' }}
          </el-button>
        </div>
        
        <el-divider content-position="left"><i class="el-icon-document"></i> 训练日志</el-divider>
        
        <!-- <div class="log-container">
          <el-scrollbar style="height: 65vh">
            <pre class="log-content">{{ fileContent || '请先选择模型并查看结果' }}</pre>
          </el-scrollbar>
        </div> -->
      <!-- 修改日志展示部分 -->
        <div class="log-container">
          <el-scrollbar style="height: 65vh">
            <div class="log-control">
              <el-pagination
                background
                layout="prev, pager, next, jumper"
                :page-size="pageSize"
                :total="totalLines"
                :current-page="currentPage"
                @current-change="handlePageChange"
                :disabled="loading"
              />
          </div>
          
          <pre class="log-content">
            {{ fileContent || '暂无日志数据' }}
            <div v-if="loading" class="loading-text">
              <i class="el-icon-loading"></i> 日志加载中...
            </div>
          </pre>
        </el-scrollbar>
      </div>

      </el-card>
    </el-col>

    <el-col :span="12" class="right-panel">
      <el-card class="image-card">
        <div class="image-control">
          <el-button 
            type="success" 
            size="medium" 
            @click="showImages"
            class="action-btn"
            :disabled="!model">
            <i class="el-icon-picture"></i> 可视化结果
          </el-button>
        </div>
        
        <el-divider content-position="left"><i class="el-icon-data-analysis"></i> 训练图表</el-divider>
        
        <el-row :gutter="20" class="image-grid">
          <el-col 
            v-for="(image, index) in images" 
            :key="index"
            :xs="24" 
            :sm="12"
            class="image-item">
            <div class="image-wrapper">
              <el-image
                :src="image"
                fit="scale-down"
                :preview-src-list="images"
                class="result-image"
                lazy>
                <div slot="placeholder" class="image-placeholder">
                  <i class="el-icon-loading"></i>
                  加载中...
                </div>
                <div slot="error" class="image-error">
                  <i class="el-icon-picture-outline"></i>
                  加载失败
                </div>
              </el-image>
              <div class="image-caption">图表 {{ index + 1 }} - {{ getImageCaption(index) }}</div>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      fileContent: '',
      currentPage: 1,
      totalPages: 1,
      pageSize: 100, // 需要与后端per_page保持一致
      totalLines: 0,
      model: '',
      images: [],
      loading: false
    }
  },
  methods: {
    async getFileContent() {
      if (!this.model) {
        this.$message.warning('请先选择模型')
        return
      }
      
      this.loading = true
      try {
        const response = await axios.get(`http://localhost:5001/logs/${this.model}`, {
          params: {
            page: this.currentPage
          }
        })

        if (response.data.status === 'success') {
          this.fileContent = response.data.content
          this.totalPages = response.data.total_pages
          // 计算总行数（近似值）
          this.totalLines = this.totalPages * this.pageSize
        } else {
          this.$notify.error({
            title: '请求错误',
            message: response.data.message || '获取日志失败',
          })
        }
      } catch (error) {
        this.handleError(error)
      } finally {
        this.loading = false
      }
    },
    handlePageChange(newPage) {
      this.currentPage = newPage
      this.getFileContent()
    },
    handleError(error) {
      const response = error.response || {};
      const data = response.data || {};
      const status = response.status;
      const message = data.message || '连接服务器失败';
      
      this.$notify.error({
        title: `错误 (${status || '网络'})`,
        message: message,
        duration: 3000
      });
    },
    getImageCaption(index) {
      const captions = {
        CNN: ["样本分布", "分类结果", "准确率曲线", "损失曲线"],
        MPINet: ["样本分布", "分类结果", "准确率曲线", "损失曲线"]
      };
      return (
        (captions[this.model] && captions[this.model][index]) 
        || "训练图表"
      );
    },
    showImages() {
      try {
        this.images = []
        const assets = {
          CNN: [
            require('@/assets/CNN_sample.png'),
            require('@/assets/CNN_result.png'),
            require('@/assets/CNN_accuracy.png'),
            require('@/assets/CNN_loss.png')
          ],
          MPINet: [
            require('@/assets/CNN_LSTM_sample.png'),
            require('@/assets/CNN_LSTM_result.png'),
            require('@/assets/CNN_LSTM_accuracy.png'),
            require('@/assets/CNN_LSTM_loss.png')
          ]
        }
        this.images = assets[this.model] || []
      } catch (error) {
        this.$notify.error({
          title: '图片加载失败',
          message: '无法加载可视化结果图片',
          duration: 3000
        })
      }
    }
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
  height: calc(100vh - 80px);
}

.left-panel, .right-panel {
  height: 100%;
}

/* 新增分页样式 */
.log-control {
  padding: 10px 0;
  background: #fff;
  position: sticky;
  top: 0;
  z-index: 1;
}

.loading-text {
  text-align: center;
  color: #909399;
  padding: 20px;
}

::v-deep .el-pagination {
  padding: 0 10px;
}

::v-deep .el-pagination.is-background .btn-next,
::v-deep .el-pagination.is-background .btn-prev {
  min-width: 32px;
}

::v-deep .el-pagination__jump {
  margin-left: 10px;
}

.result-card {
  min-height: 600px;
  height: 100%;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.image-card {
  min-height: 350px;
  height: 100%;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.control-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.model-selector {
  display: flex;
  align-items: center;
}

.selector-label {
  font-weight: 600;
  color: #606266;
  margin-right: 15px;
  font-size: 14px;
}

.model-btn {
  width: 120px;
  text-align: center;
}

.action-btn {
  width: 150px;
  letter-spacing: 1px;
}

.log-container {
  background: #f8f8f8;
  border-radius: 4px;
  padding: 15px;
  border: 1px solid #ebeef5;
}

.log-content {
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
  margin: 0;
}

.image-grid {
  /* 使用网格布局 */
  /* display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px; */
  /* 允许滚动 */
  max-height: 70vh;
  overflow-y: auto;
}

.image-item {
  margin-bottom: 20px;
  padding: 10px;
  transition: all 0.3s;
}

.result-image {
  /* width: 100%;
  height: 300px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: #fff;
  transition: transform 0.3s; */
  /* 固定图片容器高度 */
  height: 300px;
  /* 保证图片完整显示 */
  object-fit: scale-down;
  background: #f5f7fa;
}

/* 新增样式 */
.image-wrapper {
  position: relative;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  background: #fff;
  padding: 2px;
}

.image-caption {
  text-align: center;
  padding: 6px;
  font-size: 16px;
  color: #666;
  background: #f8f8f8;
  border-radius: 0 0 4px 4px;
  margin-top: -5px;
}

.image-error {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #f56c6c;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .image-grid {
    grid-template-columns: 1fr;
  }
  
  .result-image {
    height: 350px;
  }
}

.result-image:hover {
  transform: translateY(-3px);
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  font-size: 14px;
}

.el-divider__text {
  background: #fff;
  padding: 0 20px;
  color: #409EFF;
  font-weight: 500;
}
</style>