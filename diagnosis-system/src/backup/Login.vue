<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="title">核电阀门定位器故障诊断系统</h2>
      <el-form :model="inf" :rules="rules" ref="loginForm" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="inf.username" placeholder="请输入用户名" clearable></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="inf.password" type="password" placeholder="请输入密码" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="logining" @click="handleSubmit" class="full-width">登录</el-button>
        </el-form-item>
        <el-form-item>
          <el-button @click="register" class="full-width">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      logining: false,
      inf: {
        username: "",
        password: "",
      },
      rules: {
        username: [{ required: true, message: "用户名不能为空", trigger: "blur" }],
        password: [{ required: true, message: "密码不能为空", trigger: "blur" }],
      },
    };
  },
  methods: {
    register() {
      this.$router.push("/register");
    },
    handleSubmit() {
      this.$refs.loginForm.validate((valid) => {
        if (!valid) return;
        this.logining = true;
        axios.post("http://127.0.0.1:5001/login", this.inf).then((resp) => {
          this.logining = false;
          if (resp.data === "登录成功") {
            this.$message.success(`欢迎回来, ${this.inf.username}！`);
            this.$router.push("/home");
          } else {
            this.$message.error("登录失败，用户名或密码错误");
          }
        }).catch(() => {
          this.logining = false;
          this.$message.error("登录请求失败，请检查网络");
        });
      });
    },
  },
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
.login-card {
  width: 450px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.9);
}
.title {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}
.full-width {
  width: 100%;
}
</style>