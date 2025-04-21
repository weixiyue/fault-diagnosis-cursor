// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'   // router：引入 Vue 路由配置（router/index.js），用于页面导航
import jquery from "jquery";
import * as echarts from 'echarts'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios';

// 给 Vue 原型绑定全局变量
Vue.prototype.axios = axios;    // 将 axios 绑定到 Vue 原型上，使所有 Vue 组件都可以通过 this.axios 直接访问 axios 进行网络请求
Vue.prototype.$ = jquery;
Vue.prototype.$echarts = echarts

// 注册 Element UI 
Vue.use(ElementUI);   // 让 Vue 组件可以使用 Element UI 提供的组件（如 el-button、el-table 等）

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

export function checkNum(rule, value, callback) {
  if (value == '' || value == undefined || value == null) {
    callback();
  } else if (!Number(value)) {
    callback(new Error('请输入[1,20000]之间的数字'));
  } else if (value < 1 || value > 20000) {
    callback(new Error('请输入[1,20000]之间的数字'));
  } else {
    callback();
  }
}
