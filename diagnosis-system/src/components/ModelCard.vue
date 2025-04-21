<template>
    <div class="model-card">
      <h3 class="model-title">{{ model.name }} - {{ model.title }}</h3>
      
      <!-- 四图等分布局 -->
      <div class="chart-grid">
        <div 
          v-for="(type, index) in chartTypes" 
          :key="index" 
          class="chart-item"
        >
          <div class="chart-label">{{ labels[type] }}</div>
          <el-image
            :src="model.images[type]"
            :preview-src-list="previewList"
            fit="contain"
            class="chart-image"
          />
        </div>
      </div>
    </div>
</template>

<script>
export default {
    props: {
        model: {
        type: Object,
        required: true
        }
    },
    data() {
        return {
        chartTypes: ['result', 'loss', 'accuracy', 'confusion'], // 四图类型
        labels: {
            result: '预测结果',
            loss: '损失曲线',
            accuracy: '准确率曲线',
            confusion: '混淆矩阵'
        }
        }
    },
    computed: {
        previewList() {
        return Object.values(this.model.images)
        }
    }
}
</script>

<style scoped>
/* 四图等分网格 */
.chart-grid {
display: grid;
grid-template-columns: repeat(2, 1fr);  /* 2x2布局 */
gap: 16px;
}

.chart-item {
position: relative;
border: 1px solid #ebeef5;
border-radius: 6px;
padding: 12px;
background: #f8f9fa;
min-height: 250px;  /* 统一最小高度 */
}

.chart-image {
width: 100%;
height: 100%;
min-height: 200px;
}

.chart-label {
position: absolute;
top: 12px;
left: 12px;
background: rgba(255,255,255,0.9);
padding: 4px 12px;
border-radius: 4px;
font-size: 0.95em;
z-index: 1;
box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* 响应式调整 */
@media (max-width: 768px) {
.chart-grid {
    grid-template-columns: 1fr;  /* 移动端单列 */
}

.chart-item {
    min-height: 200px;
}
}
</style>