<template>
  <div class="login-container">
    <el-form
      ref="registerForm"
      :model="inf"
      :rules="rules"
      status-icon
      label-position="left"
      class="login-form"
    >
      <h2 class="title">核电阀门定位器故障诊断系统</h2>

      <el-form-item label="用户名" prop="username" class="form-label">
        <el-input v-model="inf.username" placeholder="请输入用户名" clearable />
      </el-form-item>

      <el-form-item label="密码" prop="password" class="form-label">
        <el-input v-model="inf.password" type="password" placeholder="请输入密码" show-password />
      </el-form-item>

      <el-form-item label="确认密码" prop="password2" class="form-label">
        <el-input v-model="inf.password2" type="password" placeholder="请确认密码" show-password />
      </el-form-item>

      <el-form-item label="真实姓名" prop="truename" class="form-label">
        <el-input v-model="inf.truename" placeholder="请输入真实姓名" clearable />
      </el-form-item>

      <el-form-item label="证件号" prop="idcardnum" class="form-label">
        <el-input v-model="inf.idcardnum" placeholder="请输入证件号" clearable />
      </el-form-item>

      <el-form-item class="button-group">
        <el-button type="primary" @click="register" :loading="logining">注册</el-button>
        <el-button @click="handleSubmit">已有账号？去登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from "axios";
const apiPath = 'http://127.0.0.1:5001/register';
export default {
  data() {
    return {
      logining: false,
      inf: {
        username: '',
        password: '',
        password2: '',
        truename: '',
        idcardnum: ''
      },
      rules: {
        username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
        password: [{ required: true, message: '密码不能为空', trigger: 'blur' }],
        password2: [
          { required: true, message: '确认密码不能为空', trigger: 'blur' },
          { validator: (rule, value, callback) => {
              if (value !== this.inf.password) {
                callback(new Error('两次输入的密码不一致'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ],
        truename: [{ required: true, message: '真实姓名不能为空', trigger: 'blur' }],
        idcardnum: [
          { required: true, message: '证件号不能为空', trigger: 'blur' },
          { pattern: /^\d{15}|\d{18}$/, message: '请输入正确的证件号', trigger: 'blur' }
        ],
      }
    };
  },data() {
    // 密码复杂度正则：至少8位且包含字母+数字
    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/;
    // 身份证号正则：18位，最后一位可能是X
    const idCardPattern = /^\d{17}[\dXx]$/;

    return {
      logining: false,
      showPassword: false, // 新增密码可见性状态
      inf: {
        username: '',
        password: '',
        password2: '',
        truename: '',
        idcardnum: '',
        agreed: false      // 新增隐私协议勾选
      },
      rules: {
        username: [
          { required: true, message: '用户名不能为空', trigger: 'blur' },
          { 
            min: 3, 
            max: 16, 
            message: '用户名长度需在3-16个字符之间', 
            trigger: 'blur' 
          },
          { 
            pattern: /^[a-zA-Z0-9_]+$/, 
            message: '只能包含字母、数字和下划线', 
            trigger: 'blur' 
          }
        ],
        password: [
          { required: true, message: '密码不能为空', trigger: 'blur' },
          { 
            pattern: passwordPattern, 
            message: '需至少8位且包含字母+数字', 
            trigger: 'blur' 
          }
        ],
        password2: [
          { required: true, message: '确认密码不能为空', trigger: 'blur' },
          { 
            validator: (rule, value, callback) => {
              if (value !== this.inf.password) {
                callback(new Error('两次密码不一致'));
              } else {
                callback();
              }
            }, 
            trigger: ['blur', 'change'] // 增加change触发
          }
        ],
        truename: [
          { required: true, message: '真实姓名不能为空', trigger: 'blur' },
          {
            pattern: /^[\u4e00-\u9fa5]{2,10}$/, 
            message: '请输入2-10个汉字',
            trigger: 'blur'
          }
        ],
        idcardnum: [
          { required: true, message: '证件号不能为空', trigger: 'blur' },
          { 
            pattern: idCardPattern, 
            message: '请输入18位有效身份证号', 
            trigger: 'blur' 
          }
        ],
        agreed: [ // 隐私协议验证
          {
            validator: (rule, value, callback) => {
              value ? callback() : callback(new Error('必须同意隐私政策'));
            },
            trigger: 'change'
          }
        ]
      }
    };
  },
  methods: {
    handleSubmit(){
      this.$router.push({path: '/login'});
    },
    
    register() {
      this.$refs.registerForm.validate(valid => {
        if (!valid) {
          this.$message.error("请填写完整且符合要求的注册信息");
          return;
        }

        this.logining = true;
        // 使用环境变量配置API地址
        // const apiPath = 'http://127.0.0.1:5001/register';
        
        // 过滤敏感信息日志
        const safeLogInfo = { ...this.inf };
        delete safeLogInfo.password;
        delete safeLogInfo.password2;
        console.log('注册请求数据:', safeLogInfo);

        axios.post(apiPath, this.inf)
          .then(response => {
            if (response.data.success) {
              this.$alert(`注册成功，即将跳转登录页`, '成功', {
                confirmButtonText: '确定',
                callback: () => {
                  this.$router.push("/login");
                }
              });
            } else {
              const errorMsg = response.data.message.includes('唯一约束') 
                ? '用户名已被注册' 
                : response.data.message;
              this.$message.error(errorMsg || "注册信息不符合要求");
            }
          })
          .catch(error => {
            let errorMsg = "网络异常，请检查连接";
            if (error.response) {
              errorMsg = error.response.status === 400 
                ? "请求参数错误"
                : `服务器错误（${error.response.status}）`;
            }
            this.$message.error(errorMsg);
          })
          .finally(() => {
            this.logining = false;
          });
      });
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: url("../assets/nuclear_bg.jpg") no-repeat center center;
  background-size: cover;
}

.login-form {
  width: 400px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

::v-deep(.el-form-item__label) {
  font-weight: bold;
  font-size: 16px;
}

.form-label {
  font-weight: bold; /* 加粗 */
  font-size: 16px;  /* 调整字体大小 */
}
</style>
