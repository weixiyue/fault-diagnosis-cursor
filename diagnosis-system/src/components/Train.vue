<template>
  <div class="form-container">
    <el-card shadow="hover" class="form-card">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
        <!-- 模型选择 -->
        <el-form-item label="模型类型" class="radio-form-item">
          <el-radio-group v-model="ruleForm.model" class="model-radio-group">
            <el-radio-button label="CNN" />
            <el-radio-button label="CNN_LSTM" />
          </el-radio-group>
        </el-form-item>

        <!-- 数值输入 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="样本类别" prop="num_classes">
              <el-input 
                v-model.number="ruleForm.num_classes" 
                placeholder="1-10"
                @change="validateNumber('num_classes', 1, 10)"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="迭代次数" prop="epochs">
              <el-input 
                v-model.number="ruleForm.epochs"
                placeholder="100-200"
                @change="validateNumber('epochs', 100, 200)"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="样本数量" prop="number">
              <el-input 
                v-model.number="ruleForm.number"
                placeholder="100-784"
                @change="validateNumber('number', 100, 784)"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 比例输入 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="训练集" prop="train">
              <el-input-number 
                v-model="ruleForm.train"
                :min="0"
                :max="1"
                :step="0.05"
                :precision="2"
                controls-position="right"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="验证集" prop="valid">
              <el-input-number 
                v-model="ruleForm.valid"
                :min="0"
                :max="1"
                :step="0.05"
                :precision="2"
                controls-position="right"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="测试集" prop="test">
              <el-input-number 
                v-model="ruleForm.test"
                :min="0"
                :max="1"
                :step="0.05"
                :precision="2"
                controls-position="right"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 实时校验提示 -->
        <div class="ratio-alert">
          <el-alert 
            :title="ratioStatus.text"
            :type="ratioStatus.type"
            :closable="false"
            show-icon
          />
        </div>

        <!-- 操作按钮 -->
        <el-form-item class="action-buttons">
          <el-button 
            type="primary" 
            @click="submitForm('ruleForm')" 
            :disabled="!formValid"
            :loading="isSubmitting"
          >
            {{ isSubmitting ? '训练中...' : '开始训练' }}
          </el-button>
          <el-button @click="resetForm('ruleForm')">重置参数</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";
const train = 'http://127.0.0.1:5001/train';

export default {
  name: "TrainModule",
  data() {
    return {
      isSubmitting: false,
      ruleForm: {
        num_classes: null,
        epochs: null,
        number: null,
        train: 0.6,
        valid: 0.2,
        test: 0.2,
        model: 'CNN',
      },
      rules: {
        num_classes: [
          { required: true, message: '必填项', trigger: 'blur' },
          { type: 'number', message: '必须为数字' }
        ],
        epochs: [
          { required: true, message: '必填项', trigger: 'blur' },
          { type: 'number', message: '必须为数字' }
        ],
        number: [
          { required: true, message: '必填项', trigger: 'blur' },
          { type: 'number', message: '必须为数字' }
        ],
        train: [{ required: true, message: '必填项', trigger: 'change' }],
        valid: [{ required: true, message: '必填项', trigger: 'change' }],
        test: [{ required: true, message: '必填项', trigger: 'change' }],
      },
    };
  },
  computed: {
    ratioStatus() {
      const total = Number(this.ruleForm.train) + 
                   Number(this.ruleForm.valid) + 
                   Number(this.ruleForm.test);
      const isValid = Math.abs(total - 1) < 0.0001;
      const percentage = (total * 100).toFixed(1) + '%';

      if (isValid) {
        return {
          type: 'success',
          text: `数据集比例有效 (总和: ${percentage})`
        };
      }
      return {
        type: 'error',
        text: total < 1 
          ? `数据集不足 (缺少 ${(1 - total).toFixed(2)} )` 
          : `数据集超额 (超出 ${(total - 1).toFixed(2)} )`
      };
    },
    formValid() {
      return this.ratioStatus.type === 'success' &&
        this.ruleForm.num_classes >= 1 &&
        this.ruleForm.num_classes <= 10 &&
        this.ruleForm.epochs >= 100 &&
        this.ruleForm.epochs <= 200 &&
        this.ruleForm.number >= 100 &&
        this.ruleForm.number <= 784;
    }
  },
  methods: {
    validateNumber(field, min, max) {
      const value = this.ruleForm[field];
      if (value < min) this.ruleForm[field] = min;
      if (value > max) this.ruleForm[field] = max;
    },
    async submitForm(formName) {
      this.isSubmitting = true;
      try {
        const response = await axios.post(train, this.ruleForm);
        if (response.data.success) {
          this.$message.success('模型训练启动成功');
          this.$router.push('/result');
        }
      } catch (error) {
        this.$message.error(`训练失败: ${error.message}`);
      } finally {
        this.isSubmitting = false;
      }
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
      this.ruleForm.train = 0.6;
      this.ruleForm.valid = 0.2;
      this.ruleForm.test = 0.2;
    }
  }
};
</script>

<style scoped>
.form-container {
  padding: 20px;
  display: flex;
  justify-content: center;
  background: #f5f7fa;
  min-height: calc(60vh - 60px);
}

.form-card {
  width: 800px;
  margin-top: 40px;
  border-radius: 8px;
}

/* .model-select {
  margin: 15px 0 25px;
} */

.radio-form-item {
  ::v-deep .el-form-item__content {
    display: flex;
    align-items: center;  /* 垂直居中 */
    height: 40px;         /* 保持与输入框相同高度 */
  }
  
  ::v-deep .el-form-item__label {
    padding: 0 12px 0 0;  /* 调整标签间距 */
    line-height: 40px;     /* 与内容区同高 */
  }
}

/* 单选按钮组微调 */
.model-radio-group {
  margin-top: -2px;  /* 视觉补偿对齐 */
  
  .el-radio-button {
    &:first-child .el-radio-button__inner {
      border-radius: 4px 0 0 4px;
    }
    &:last-child .el-radio-button__inner {
      border-radius: 0 4px 4px 0;
    }
  }
}

.el-input-number {
  width: 100%;
}

.ratio-alert {
  margin: 20px 0;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
}

.el-row {
  margin-bottom: 15px;
}

.el-form-item {
  margin-bottom: 18px;
}
</style>