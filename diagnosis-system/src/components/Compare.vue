<template>
  <el-container class="container">
    <!-- 头部信息 -->
    <el-header class="header">
      <el-card shadow="hover" class="info-card">
        <div class="info-grid">
          <div class="info-item">
            <span class="label">模型数据集：</span>
            <el-tag type="success">DAMADICS</el-tag>
          </div>
          <div class="info-item">
            <span class="label">样本类别：</span>
            <el-tag>10类</el-tag>
          </div>
          <div class="info-item">
            <span class="label">样本维度：</span>
            <el-tag>784</el-tag>
          </div>
          <div class="info-item">
            <span class="label">每类样本数：</span>
            <el-tag type="warning">300</el-tag>
          </div>
          <div class="info-item">
            <span class="label">数据划分：</span>
            <el-tag type="danger">8:1:1</el-tag>
          </div>
          <div class="info-item">
            <span class="label">迭代次数：</span>
            <el-tag type="info">100</el-tag>
          </div>
        </div>
      </el-card>
    </el-header>

    <!-- 主体内容 -->
    <el-main class="main-content">
      <!-- 数据预览 -->
      <el-card shadow="hover" class="data-preview">
        <h3 class="section-title">数据分布预览</h3>
        <el-image 
          :src="require('@/assets/compare/data.png')" 
          :preview-src-list="[require('@/assets/compare/data.png')]"
          fit="contain"
          class="preview-image"
        />
      </el-card>

      <!-- 模型对比 -->
      <div class="model-comparison">
        <el-row :gutter="20">
          <el-col 
            v-for="(model, index) in models"
            :key="index"
            :xs="24" :sm="12" :md="12" :lg="12" :xl="12"
            class="model-col"
          >
            <model-card :model="model"/>
          </el-col>
        </el-row>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import ModelCard from '@/components/ModelCard.vue'

export default {
  components: { ModelCard },
  data() {
    return {
      models: [
        {
          name: 'CNN',
          title: '一维卷积神经网络',
          images: {
            result: require('@/assets/compare/CNN_result.png'),
            loss: require('@/assets/compare/CNN_loss.png'),
            accuracy: require('@/assets/compare/CNN_accuracy.png'),
            confusion: require('@/assets/compare/CNN_confusion.png')
          }
        },
        {
          name: 'Inception',
          title: '深度循环神经网络',
          images: {
            result: require('@/assets/compare/Inception_result.png'),
            loss: require('@/assets/compare/Inception_loss.png'),
            accuracy: require('@/assets/compare/Inception_accuracy.png'),
            confusion: require('@/assets/compare/Inception_confusion.png')
          }
        },
        {
          name: 'LSTM',
          title: '长短期记忆神经网络',
          images: {
            result: require('@/assets/compare/LSTM_result.png'),
            loss: require('@/assets/compare/LSTM_loss.png'),
            accuracy: require('@/assets/compare/LSTM_accuracy.png'),
            confusion: require('@/assets/compare/LSTM_confusion.png')
          }
        },
        {
          name: 'GRU',
          title: '门控循环单元网络',
          images: {
            result: require('@/assets/compare/GRU_result.png'),
            loss: require('@/assets/compare/GRU_loss.png'),
            accuracy: require('@/assets/compare/GRU_accuracy.png'),
            confusion: require('@/assets/compare/GRU_confusion.png')
          }
        }
      ]
    }
  }
}
</script>

<style scoped>
.container {
  height: 100vh;
  background: #f5f7fa;
}

.header {
  height: auto !important;
  padding: 20px;
}

.info-card {
  border-radius: 8px;
  background: linear-gradient(145deg, #f8f9fa, #ffffff);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  padding: 10px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.label {
  font-weight: 500;
  color: #606266;
}

.main-content {
  padding: 20px;
}

.data-preview {
  margin-bottom: 24px;
  transition: transform 0.3s;
}

.data-preview:hover {
  transform: translateY(-3px);
}

.section-title {
  text-align: center;
  color: #303133;
  margin: 16px 0;
  font-weight: 600;
  position: relative;
  padding-bottom: 8px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 2px;
  background: #409eff;
}

.preview-image {
  width: 100%;
  height: 400px;
  border-radius: 6px;
  transition: all 0.3s;
}

.model-comparison {
  margin-top: 20px;
}

.model-col {
  margin-bottom: 20px;
}
</style>