<template>
  <div class="form-container">
    <el-card class="form-card" shadow="hover">
      <div class="form-title">数据集上传</div>
      <el-form 
        :model="ruleForm" 
        :rules="rules" 
        ref="ruleForm" 
        label-width="100px" 
        class="demo-ruleForm"
        label-position="top"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="数据集ID" prop="id">
              <el-input 
                v-model.number="ruleForm.id" 
                type="number"
                placeholder="请输入数字类型ID"
                :min="1"
                :controls="false"
                @keydown.native.prevent="handleKeydown"
              >
                <template #append>
                  <el-tooltip content="ID需为大于0的整数">
                    <i class="el-icon-info"></i>
                  </el-tooltip>
                </template>
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="数据集名称" prop="name">
              <el-input 
                v-model="ruleForm.name" 
                placeholder="请输入数据集名称"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属地区" prop="region">
              <el-select 
                v-model="ruleForm.region" 
                placeholder="请选择地区"
                style="width: 100%"
                clearable
              >
                <el-option
                  v-for="item in regions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系方式" prop="contact">
              <el-input 
                v-model="ruleForm.contact" 
                placeholder="请输入手机或邮箱"
                clearable
              >
                <template #prefix>
                  <i class="el-icon-message"></i>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="数据集描述" prop="description">
          <el-input
            v-model="ruleForm.description"
            type="textarea"
            :rows="3"
            placeholder="请简要描述数据集内容"
            maxlength="200"
            show-word-limit
          ></el-input>
        </el-form-item>

        <el-form-item label="是否启用" prop="ischoosed">
          <el-switch
            v-model="ruleForm.ischoosed"
            active-text="启用"
            inactive-text="停用"
            active-color="#13ce66"
          ></el-switch>
        </el-form-item>

        <el-form-item label="数据文件上传">
          <el-upload
            class="data-uploader"
            :limit="1"
            :file-list="fileList"
            :auto-upload="true"
            action="http://127.0.0.1:5001/uploadDatafile"
            :data="{ datasetId: ruleForm.id }"
            :before-upload="validateUpload"
            accept=".mat"
            @success="handleUploadSuccess"
            @error="handleUploadError"
          >
            <template #trigger>
              <el-button type="primary" icon="el-icon-upload">选择文件</el-button>
            </template>
            <div class="upload-tip">
              <i class="el-icon-info"></i> 支持MAT格式文件，大小不超过500MB
            </div>
          </el-upload>
        </el-form-item>

        <el-form-item class="form-actions">
          <el-button 
            type="success" 
            @click="submitForm('ruleForm')"
            icon="el-icon-check"
          >提交添加</el-button>
          <el-button 
            @click="resetForm('ruleForm')"
            icon="el-icon-refresh"
          >重置表单</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";
const path = 'http://127.0.0.1:5001/uploadDataset';
// const makdir = 'http://127.0.0.1:5001/makeDatadir';

export default {
  name: "UploadData",
  data() {
    const validateId = (rule, value, callback) => {
      if (!Number.isInteger(value) || value <= 0) {
        callback(new Error('ID必须为正整数'));
      } else {
        callback();
      }
    };
    return {
      fileList: [],
      uploadData: { 'name': '' },
      regions: [
        { value: '华东', label: '华东地区' },
        { value: '华北', label: '华北地区' },
        { value: '华南', label: '华南地区' },
        { value: '西南', label: '西南地区' },
      ],
      ruleForm: {
        id: '',
        name: '',
        region: '',
        contact: '',
        description: '',
        ischoosed: true
      },
      rules: {
        id: [
          { required: true, message: 'ID不能为空' },
          { validator: validateId, trigger: 'blur' }
        ],
        name: [
          { required: true, message: '数据集名称不能为空', trigger: 'blur' },
          { max: 32, message: '名称长度不能超过32字符', trigger: 'blur' }
        ],
        contact: [
          { required: true, message: '联系方式不能为空', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$|^\w+@\w+\.\w+$/, message: '格式应为手机号或邮箱', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '描述信息不能为空', trigger: 'blur' },
          { min: 10, message: '描述至少需要10个字符', trigger: 'blur' }
        ]
      },
    };
  },
  methods: {
    validateUpload() {
      if (!this.ruleForm.id) {
        this.$message.error('请先填写数据集ID');
        return false;
      }
      this.uploadData.datasetId = this.ruleForm.id;
      return true;
    },
    handleKeydown(e) {
      // 禁止输入非数字字符
      const invalidKeys = ['e', 'E', '+', '-', '.'];
      if (invalidKeys.includes(e.key)) {
        e.preventDefault();
      }
    },
    // 在submitForm中统一处理
    async submitForm() {
      try {
        // 先提交表单数据
        const resp = await axios.post(path, this.ruleForm);
        
        // 自动触发文件上传（如果已选择文件）
        if (this.fileList.length > 0) {
          await this.$refs.upload.submit();
        }
        
        this.$message.success('数据集创建成功');
      } catch (error) {
        this.$message.error('操作失败');
      }
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
      this.fileList = [];
    },
    handleUploadSuccess(response) {
      if (response.code === 200) {
        this.$message.success(`文件上传成功: ${response.fileName}`);
      }
    },
    handleUploadError(err) {
      this.$message.error(`文件上传失败: ${err.message}`);
    }
  }
}
</script>

<style scoped>
.form-container {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

.form-card {
  width: 800px;
  border-radius: 8px;
  transition: all 0.3s;
}

.form-title {
  font-size: 20px;
  color: #303133;
  font-weight: 600;
  margin-bottom: 30px;
  text-align: center;
  letter-spacing: 1px;
}

.data-uploader {
  border: 1px dashed #409EFF;
  border-radius: 6px;
  padding: 20px;
  text-align: center;
  background-color: #fafafa;
}

.upload-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 10px;
}

.form-actions {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.el-form-item {
  margin-bottom: 22px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}
</style>