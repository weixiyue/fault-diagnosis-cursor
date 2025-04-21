<template>
  <el-container style="min-height: 100vh;">
    <!-- 顶部标题 -->
    <el-header class="header-content">
      <h1 class="header-title">
        使用的模型数据集：样本类别10、样本长度784、每类300个样本（标准化）、迭代次数100次，训练集、验证集、测试集比例8:1:1
      </h1>
    </el-header>

    <!-- 主体内容 -->
    <el-main>
      <!-- 数据集展示图 -->
      <el-row :gutter="20" class="mb-20">
        <el-col :span="24">
          <!-- <el-image
            :src="require('@/assets/compare/data.png')"
            :fit="fit"
            :preview-src-list="images"
            class="data-image"
          ></el-image> -->
        </el-col>
      </el-row>

      <!-- 第一行：CNN 与 Inception 模型 -->
      <el-row :gutter="20" class="mb-20">
        <el-col :xs="24" :sm="12">
          <el-card shadow="hover" class="model-card">
            <h2 class="model-title">CNN 一维卷积神经网络</h2>
            <div class="card-images">
              <el-image :src="require('@/assets/compare/CNN_result.png')" :fit="contain" :preview-src-list=images class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/CNN_loss.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/CNN_accuracy.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/CNN_confusion.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12">
          <el-card shadow="hover" class="model-card">
            <h2 class="model-title">Inception 深度循环神经网络</h2>
            <div class="card-images">
              <el-image :src="require('@/assets/compare/Inception_result.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/Inception_loss.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/Inception_accuracy.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/Inception_confusion.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 第二行：LSTM 与 GRU 模型 -->
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12">
          <el-card shadow="hover" class="model-card">
            <h2 class="model-title">LSTM 长短期记忆网络</h2>
            <div class="card-images">
              <el-image :src="require('@/assets/compare/LSTM_result.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/LSTM_loss.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/LSTM_accuracy.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/LSTM_confusion.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12">
          <el-card shadow="hover" class="model-card">
            <h2 class="model-title">GRU 深度循环神经网络</h2>
            <div class="card-images">
              <el-image :src="require('@/assets/compare/GRU_result.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/GRU_loss.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/GRU_accuracy.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
              <el-image :src="require('@/assets/compare/GRU_confusion.png')" :fit="contain" :preview-src-list="images" class="model-image"></el-image>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      fit: 'cover',
      images: [
            // require('@/assets/compare/CNN_confusion.png'),
            // require('@/assets/compare/CNN_result.png'),
            // require('@/assets/compare/CNN_accuracy.png'),
            // require('@/assets/compare/CNN_loss.png'),
            // require('@/assets/compare/LSTM_confusion.png'),
            // require('@/assets/compare/LSTM_result.png'),
            // require('@/assets/compare/LSTM_accuracy.png'),
            // require('@/assets/compare/LSTM_loss.png'),
            // require('@/assets/compare/INCEPTION_confusion.png'),
            // require('@/assets/compare/INCEPTION_result.png'),
            // require('@/assets/compare/INCEPTION_accuracy.png'),
            // require('@/assets/compare/INCEPTION_loss.png'),
            // require('@/assets/compare/GRU_confusion.png'),
            // require('@/assets/compare/GRU_result.png'),
            // require('@/assets/compare/GRU_accuracy.png'),
            // require('@/assets/compare/GRU_loss.png')
          ],
    }
  },
}
</script>

<style scoped>
/* 顶部标题 */
.header-content {
  background-color: #673ab7;
  padding: 20px;
  text-align: center;
  color: #fff;
}
.header-title {
  margin: 0;
  font-size: 24px;
}

/* 数据图样式 */
.data-image {
  width: 100%;
  max-height: 500px;
  object-fit: cover;
  border-radius: 4px;
}

/* 卡片及图片布局 */
.model-card {
  margin-bottom: 20px;
}
.model-title {
  font-size: 20px;
  margin-bottom: 10px;
  text-align: center;
}
.card-images {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
/* .model-image {
  width: 48%;
  margin-bottom: 10px;
  border-radius: 4px;
  
  transition: transform 0.3s;
} */
.model-image {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.model-image:hover {
  transform: scale(1.05);
}

/* 辅助间距 */
.mb-20 {
  margin-bottom: 20px;
}

</style>
