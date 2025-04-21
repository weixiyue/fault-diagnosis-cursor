<template>
  <div class="table-container">
    <el-table
      :data="tableData"
      border
      stripe
      header-row-class-name="table-header"
      row-class-name="table-row"
      style="width: 100%"
      class="responsive-table"
    >
      <el-table-column
        prop="id"
        label="序号"
        width="100"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="name"
        label="数据集提供者"
        min-width="120"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="region"
        label="国家/地区"
        width="120"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="contact"
        label="联系方式"
        min-width="220"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="description"
        label="简介"
        min-width="200"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="ischoosed"
        label="选中状态"
        width="120"
        align="center"
      >
        <template slot-scope="scope">
          <el-tag
            :type="scope.row.ischoosed ? 'success' : 'danger'"
            effect="dark"
          >
            {{ scope.row.ischoosed ? "已选中" : "未选中" }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120" align="center">
        <template slot-scope="scope">
          <el-button
            size="mini"
            :type="scope.row.ischoosed ? 'danger' : 'primary'"
            @click="toggleSelection(scope.row)"
          >
            {{ scope.row.ischoosed ? "取消" : "选择" }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "axios";
const API = {
  show: 'http://127.0.0.1:5001/showDataset',
  update: 'http://127.0.0.1:5001/updateDataset'
};

export default {
  name: "ExistedData",
  created() {
    this.fetchData();
  },
  data() {
    return {
      tableData: []
    };
  },
  methods: {
    async fetchData() {
      try {
        const { data } = await axios.get(API.show);
        this.tableData = data.map(item => ({
          ...item,
          ischoosed: Boolean(item.ischoosed)
        }));
      } catch (error) {
        this.$message.error('数据加载失败');
      }
    },
    async toggleSelection(row) {
      try {
        const newStatus = !row.ischoosed;
        await axios.post(API.update, {
          id: row.id,  // 传递记录ID
          status: newStatus
        });
        row.ischoosed = newStatus;
        this.$message.success('状态更新成功');
      } catch (error) {
        this.$message.error('状态更新失败');
      }
    }
  }
};
</script>

<style scoped>
.table-container {
  padding: 30px 40px;
}

.responsive-table {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

@media screen and (max-width: 1200px) {
  .table-container {
    padding: 20px;
  }
}

/deep/ .table-header th {
  background-color: #f8f9fa !important;
  color: #343a40;
  font-weight: 600;
  padding: 12px 0;
}

/deep/ .table-row td {
  padding: 10px 0;
  transition: background-color 0.3s;
}

/deep/ .el-table--striped .table-row:nth-child(2n) td {
  background-color: #f8f9fa;
}

/deep/ .el-table__body tr:hover td {
  background-color: #e9ecef !important;
}
</style>