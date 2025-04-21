<template>
  <el-container class="home_container">
    <!-- 头部样式优化 -->
    <el-header class="system-header">
      <div class="home_title">
        <i class="el-icon-s-operation"></i>
        核电阀门定位器故障诊断系统
      </div>
    </el-header>

    <el-container>
      <!-- 侧边栏样式优化 -->
      <el-aside width="220px" class="system-aside">
        <el-menu
          router
          class="nuclear-menu"
          background-color="#1f2d3d"
          text-color="#b7c3d3"
          active-text-color="#409EFF"
        >
          <el-submenu index="data-group">
            <template slot="title">
              <i class="el-icon-folder-opened"></i>
              <span>数据管理</span>
            </template>
            <el-menu-item index="/home/existeddata">
              <i class="el-icon-document-checked"></i>
              <span>历史数据调取</span>
            </el-menu-item>
            <el-menu-item index="/home/uploaddata">
              <i class="el-icon-upload2"></i>
              <span>实时数据接入</span>
            </el-menu-item>
          </el-submenu>

          <el-menu-item index="/home/train">
            <i class="el-icon-cpu"></i>
            <span>智能诊断训练</span>
          </el-menu-item>

          <el-menu-item index="/home/result">
            <i class="el-icon-data-analysis"></i>
            <span>诊断结果分析</span>
          </el-menu-item>

          <el-menu-item index="/home/compare">
            <i class="el-icon-notebook-2"></i>
            <span>模型效能对比</span>
          </el-menu-item>

          <el-menu-item index="/home/help">
            <i class="el-icon-guide"></i>
            <span>系统操作指南</span>
          </el-menu-item>

          <el-menu-item index="/login" class="logout-item">
            <i class="el-icon-switch-button"></i>
            <span>安全退出系统</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-container>
        <!-- 主内容区优化 -->
        <el-main class="system-main">
          <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/Home' }">
              <i class="el-icon-s-home"></i>主控台
            </el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRouteName }}</el-breadcrumb-item>
          </el-breadcrumb>

          <!-- <div class="dashboard-panel">
            <el-image 
              :src="require('@/assets/nuclear-flow.jpg')" 
              :fit="fit"
              class="system-schematic"
              :preview-src-list="images">
            </el-image>
            <h2 class="process-title">阀门定位器监测流程</h2>
            <router-view></router-view>
          </div> -->

          <div class="dashboard-panel">
            <!-- 新增v-if条件判断 -->
            <div v-if="isHomeDashboard">
              <el-image 
                :src="require('@/assets/SystemFlow.svg')" 
                :fit="fit"
                class="system-schematic"
                :preview-src-list="images">
              </el-image>
              <h2 class="process-title">阀门定位器故障诊断系统使用流程</h2>
            </div>
            
            <router-view></router-view>
          </div>
          

        </el-main>

        <!-- 页脚优化 -->
        <el-footer class="system-footer">
          <span>核安监测平台 © 2024 核电智能诊断技术中心</span>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'NuclearHome',
  computed: {
    currentRouteName() {
      return this.$route.meta.title || this.$route.name || '监控看板';
    },
     // 新增计算属性
    isHomeDashboard() {
    return this.$route.path === '/home' || 
            this.$route.path === '/home/' || 
            this.$route.name === 'Home';
    }
  }
};
</script>

<style lang="scss" scoped>
.home_container {
  height: 100vh;
  background: #f0f4f9;

  .system-header {
    background: linear-gradient(145deg, #1f2d3d, #324157);
    height: 60px !important;
    display: flex;
    align-items: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);

    .home_title {
      color: #fff;
      font-size: 24px;
      letter-spacing: 1.5px;
      display: flex;
      align-items: center;

      i {
        margin-right: 12px;
        font-size: 28px;
      }
    }
  }

  .system-aside {
    background: #1f2d3d;
    transition: all 0.3s;

    .nuclear-menu {
      .el-submenu__title, .el-menu-item {
        height: 48px !important;
        line-height: 48px !important;
        font-size: 18px;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        
        &:hover {
          background-color: #2b3a4d !important;
          transform: translateX(5px);
        }
        
        i {
          margin-right: 12px;
          font-size: 18px;  /* 放大图标 */
        }
      }

      .el-submenu__title {
        span {
          font-size: 18px;  /* 可调整具体数值 */
          font-weight: 500;
          color: #b7c3d3;
        }
        
        // .el-icon-folder-opened {
        //   font-size: 18px;  /* 匹配字体大小 */
        //   vertical-align: middle;
        //   margin-right: 12px;
        // }
      }
      
      /* 保持其他菜单项样式统一 */
      // .el-menu-item span {
      //   font-size: 15px;
      // }

      .menu-group-title {
        font-weight: 600;
        letter-spacing: 0.5px;
      }

      /* 增加菜单项间隔 */
      .el-menu-item {
        margin: 4px 0;
        border-radius: 6px;
        
        &.is-active {
          background-color: #b6cadf !important;
          box-shadow: 2px 0 8px rgba(64,158,255,0.3);
          font-weight: 700 !important;
          font-size: 20px;
          letter-spacing: 0.5px;
          color: #1a1919 !important;
        }
      }

      /* 退出按钮特殊样式 */
      .logout-item {
        position: absolute;
        bottom: -100px;
        width: calc(100%);
        margin: 0 0px;
        border-top: 1px solid #2b3a4d;
        background-color: #89c8db !important;
        color: #deeff18a !important;
        
        &:hover {
          background-color: #f39291 !important;
          font-weight: 700 !important;
          font-size: 20px;
          color: #0112148a !important;
        }
      }
   }
  }

  .system-main {
    padding: 20px;
    background: #f5f7fa;

    .dashboard-panel {
      background: #fff;
      border-radius: 8px;
      padding: 24px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.05);
      min-height: calc(100vh - 140px);

      .system-schematic {
        width: 80%;
        margin: 20px auto;
        border: 1px solid #ebeef5;
        border-radius: 4px;
      }

      .process-title {
        color: #1f2d3d;
        margin: 20px 0;
        font-weight: 500;
      }
    }

    .el-breadcrumb {
      margin-bottom: 20px;
      font-size: 16px;
    }
  }

  .system-footer {
    background: #1f2d3d;
    color: #d5dbe2;
    height: 50px !important;
    line-height: 50px;
    font-size: 15px;
    letter-spacing: 1px;
  }
}
</style>