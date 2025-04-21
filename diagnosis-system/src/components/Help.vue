<template>
  <div class="enhanced-info-container">
    <!-- 技术支持卡片 -->
    <el-card class="info-card support-card">
      <div class="card-header">
        <i class="el-icon-service gradient-icon"></i>
        <h3>技术支持渠道</h3>
        <span class="status-badge">7×24 小时在线</span>
      </div>
      
      <div class="info-grid">
        <div class="info-item" @mouseenter="hoverEffect">
          <div class="icon-wrapper bg-blue">
            <i class="el-icon-phone"></i>
          </div>
          <div class="info-content">
            <div class="info-label">紧急联络</div>
            <div class="info-value">
              +86 400-888-1999
              <el-tag type="success" size="mini" effect="dark">中文服务</el-tag>
            </div>
          </div>
          <el-button 
            class="copy-btn"
            type="text"
            @click="copyText('400-888-1999')"
            icon="el-icon-copy-document">
          </el-button>
        </div>

        <div class="info-item" @mouseenter="hoverEffect">
          <div class="icon-wrapper bg-purple">
            <i class="el-icon-message"></i>
          </div>
          <div class="info-content">
            <div class="info-label">技术邮箱</div>
            <div class="info-value">
              support@nuclearai.com
              <el-tooltip content="平均响应时间<2小时" placement="top">
                <i class="el-icon-alarm-clock"></i>
              </el-tooltip>
            </div>
          </div>
          <el-button 
            class="copy-btn"
            type="text"
            @click="copyText('support@nuclearai.com')"
            icon="el-icon-copy-document">
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 系统信息卡片 -->
    <el-card class="info-card system-card">
      <div class="card-header">
        <i class="el-icon-monitor gradient-icon"></i>
        <h3>系统状态监控</h3>
        <el-tag type="success" effect="plain">运行正常</el-tag>
      </div>

      <div class="system-grid">
        <div class="system-item">
          <div class="version-badge">
            <span class="version-text">V2.3.1</span>
            <span class="build-number">Build 202403</span>
          </div>
          <div class="update-info">
            <div class="info-label">最后更新</div>
            <div class="info-value">
              <i class="el-icon-time"></i>
              2024-03-15 14:30:00
            </div>
          </div>
        </div>

        <div class="status-indicator">
          <div class="indicator-item">
            <div class="indicator-label">API服务</div>
            <el-progress 
              :percentage="85" 
              :show-text="false"
              status="success"
              :stroke-width="8">
            </el-progress>
          </div>
          <div class="indicator-item">
            <div class="indicator-label">数据库</div>
            <el-progress 
              :percentage="100" 
              :show-text="false"
              status="success"
              :stroke-width="8">
            </el-progress>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  methods: {
    copyText(text) {
      navigator.clipboard.writeText(text).then(() => {
        this.$notify({
          title: '复制成功',
          message: '信息已存入剪贴板',
          type: 'success',
          duration: 1500
        });
      });
    },
    hoverEffect(event) {
      event.currentTarget.style.transform = 'translateY(-2px)';
      setTimeout(() => {
        event.currentTarget.style.transform = 'none';
      }, 300);
    }
  }
}
</script>

<style lang="scss" scoped>
.enhanced-info-container {
  display: grid;
  gap: 24px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;

  .info-card {
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    transition: transform 0.3s ease;

    &:hover {
      transform: translateY(-3px);
    }

    .card-header {
      display: flex;
      align-items: center;
      padding-bottom: 16px;
      margin-bottom: 20px;
      border-bottom: 1px solid #eee;

      .gradient-icon {
        font-size: 28px;
        background: linear-gradient(135deg, #409EFF, #67C23A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-right: 12px;
      }

      h3 {
        font-size: 20px;
        color: #2c3e50;
        margin-right: 15px;
      }

      .status-badge {
        background: #f0f9eb;
        color: #67c23a;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 12px;
      }
    }
  }

  .info-grid {
    display: grid;
    gap: 16px;

    .info-item {
      display: flex;
      align-items: center;
      padding: 18px;
      background: #f8f9fa;
      border-radius: 8px;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

      &:hover {
        background: #fff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
      }

      .icon-wrapper {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 16px;

        i {
          color: white;
          font-size: 18px;
        }

        &.bg-blue { background: #409EFF; }
        &.bg-purple { background: #a855f7; }
      }

      .info-content {
        flex: 1;

        .info-label {
          color: #6b7280;
          font-size: 12px;
          margin-bottom: 4px;
        }

        .info-value {
          font-size: 16px;
          font-weight: 500;
          color: #1f2937;
          display: flex;
          align-items: center;
          gap: 8px;
        }
      }

      .copy-btn {
        padding: 8px;
        margin-left: 12px;
        opacity: 0.6;
        transition: all 0.3s;

        &:hover {
          opacity: 1;
          transform: scale(1.1);
        }
      }
    }
  }

  .system-card {
    .system-grid {
      display: grid;
      grid-template-columns: 1fr 2fr;
      gap: 30px;

      .version-badge {
        background: #f5f7fa;
        padding: 16px;
        border-radius: 8px;
        text-align: center;

        .version-text {
          display: block;
          font-size: 24px;
          font-weight: 700;
          color: #3b82f6;
        }

        .build-number {
          font-size: 12px;
          color: #6b7280;
        }
      }

      .update-info {
        margin-top: 20px;

        .info-label {
          color: #6b7280;
          font-size: 12px;
        }

        .info-value {
          font-size: 14px;
          color: #374151;
          display: flex;
          align-items: center;
          gap: 8px;
          margin-top: 6px;
        }
      }

      .status-indicator {
        .indicator-item {
          margin-bottom: 20px;

          .indicator-label {
            color: #4b5563;
            font-size: 13px;
            margin-bottom: 8px;
          }
        }
      }
    }
  }

  @media (max-width: 768px) {
    .system-grid {
      grid-template-columns: 1fr !important;
    }
  }
}
</style>