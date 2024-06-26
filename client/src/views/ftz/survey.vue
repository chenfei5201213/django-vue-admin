<template>
  <div class="app-container">
    <el-card>
      <div>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增问卷</el-button>
        <el-select v-model="listQuery.type"
                   placeholder="课程类型"
                   clearable
                   style="width: 120px">
          <el-option v-for="(item, index) in typeOptions" :key="index" :label="item.name"
                     :value="item.value"></el-option>
        </el-select>
        <el-input
        v-model="listQuery.search"
        placeholder="输入问卷标题进行搜索"
        style="width: 300px"
        class="filter-item"
        @keyup.native="handleFilter"
      />
        <el-button
          class="filter-item"
          type="primary"
          icon="el-icon-search"
          @click="resetFilter"
        >查询
        </el-button
        >
      </div>
    </el-card>

    <el-table
      v-loading="listLoading"
      :data="
        tableDataList.results.filter(
          (data) =>
            !search || data.title.toLowerCase().includes(search.toLowerCase())
        )
      "
      style="width: 100%; margin-top: 10px"
      highlight-current-row
      row-key="id"
      height="100"
      stripe
      border
      v-el-height-adaptive-table="{ bottomOffset: 50 }"
    >
      <el-table-column label="ID" width="60">
        <template slot-scope="scope">{{ scope.row.id }}</template>
      </el-table-column>
      <el-table-column label="问卷标题">
        <template slot-scope="scope">{{ scope.row.title }}</template>
      </el-table-column>
      <el-table-column label="问卷描述">
        <template slot-scope="scope">{{ scope.row.description }}</template>
      </el-table-column>
      <el-table-column label="开始时间">
        <template slot-scope="scope">{{ scope.row.start_time }}</template>
      </el-table-column>
      <el-table-column label="结束时间">
        <template slot-scope="scope">{{ scope.row.expiry_time }}</template>
      </el-table-column>
      <el-table-column label="创建日期">
        <template slot-scope="scope">
          <span>{{ scope.row.create_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="更新时间">
        <template slot-scope="scope">
          <span>{{ scope.row.update_time }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="mini"
            icon="el-icon-edit"
            :disabled="!checkPermission(['position_update'])"
            @click="handleEdit(scope)"
          />
          <el-button
            type="success"
            size="mini"
            :disabled="!checkPermission(['position_update'])"
            @click="goToQuestionsPage(scope)">
            录入问题
          </el-button>
          <el-button
            type="info"
            size="mini"
            :disabled="!checkPermission(['position_update'])"
            @click="handleEdit(scope)">
            调查结果
          </el-button>
          <el-button
            type="danger"
            size="mini"
            icon="el-icon-delete"
            :disabled="!checkPermission(['position_delete'])"
            @click="handleDelete(scope)"
          />
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
            v-show="tableDataList.count>0"
            :total="tableDataList.count"
            :page-size.sync="listQuery.page_size"
            :layout="prev,pager,next"
            :current-page.sync="listQuery.page"
            @current-change="getList"
          ></el-pagination>
    <el-dialog
      :visible.sync="dialogVisible"
      :title="dialogType === 'edit' ? '编辑问卷' : '新增问卷'"
    >
      <el-form
        ref="Form"
        :model="tableData"

        label-width="80px"
        label-position="right"
      >
        <el-form-item label="问卷标题" prop="title">
          <el-input v-model="tableData.title" placeholder="问卷标题"/>
        </el-form-item>
        <el-form-item label="问卷描述" prop="description">
          <el-input v-model="tableData.description" placeholder="问卷描述"/>
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker v-model="tableData.start_time" placeholder="课时数量" type="datetime"/>
        </el-form-item>
        <el-form-item label="结束时间" prop="expiry_time">
          <el-date-picker v-model="tableData.expiry_time" placeholder="结束时间" type="datetime"/>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button type="danger" @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirm('Form')">确认</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {
  getSurveyById,
  getSurveyList,
  createSurvey,
  updateSurvey,
  deleteSurvey
} from "@/api/survey";
import {genTree, deepClone} from "@/utils";
import checkPermission from "@/utils/permission";
import {getEnumConfigList} from "@/api/enum_config";

const defaultM = {
  title: "",
  description: ""
};
export default {
  data() {
    return {
      tableData: {
        id: "",
        title: "",
        description: "",
        start_time: "",
        expiry_time: "",
        create_time: "",
        update_time: ""
      },
      search: "",
      tableDataList: {},
      listLoading: true,
      dialogVisible: false,
      dialogType: "new",
      typeOptions: [],
      listQuery: {
        page: 1,
        page_size: 20,
        search: null
      },
      enumConfigQuery: {
        module: 'course',
        service: 'type'
      }
    };
  },
  computed: {},
  created() {
    this.getCourseTypeList();
    this.getList();
  },
  methods: {
    checkPermission,
    getCourseTypeList(){
      getEnumConfigList(this.enumConfigQuery).then((response) => {
        this.typeOptions = response.data.results;
      })
    },
    getList() {
      this.listLoading = true;
      getSurveyList(this.listQuery).then((response) => {
        this.tableDataList = response.data;
        this.tableData = response.data;
        this.listLoading = false;
      });
    },
    resetFilter() {
      this.getList();
    },
    handleFilter() {
      const newData = this.tableDataList.filter(
        (data) =>
          !this.search ||
          data.title.toLowerCase().includes(this.search.toLowerCase())
      );
      this.tableData = genTree(newData);
    },
    handleAdd() {
      this.tableData = Object.assign({}, defaultM);
      this.dialogType = "new";
      this.dialogVisible = true;
      this.$nextTick(() => {
        this.$refs["Form"].clearValidate();
      });
    },
    handleEdit(scope) {
      this.tableData = Object.assign({}, scope.row); // copy obj
      this.dialogType = "edit";
      this.dialogVisible = true;
      this.$nextTick(() => {
        this.$refs["Form"].clearValidate();
      });
    },
    handleDelete(scope) {
      this.$confirm("确认删除?", "警告", {
        confirmButtonText: "确认",
        cancelButtonText: "取消",
        type: "error",
      })
        .then(async () => {
          await deleteSurvey(scope.row.id);
          this.getList();
          this.$message({
            type: "success",
            message: "成功删除!",
          });
        })
        .catch((err) => {
          console.error(err);
        });
    },
    goToQuestionsPage(scope){
      this.$router.push({ name: 'questions', params: scope });
    },
    async confirm(form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          const isEdit = this.dialogType === "edit";
          if (isEdit) {
            updateSurvey(this.tableData.id, this.tableData).then(() => {
              this.getList();
              this.dialogVisible = false;
              this.$message({
                message: "编辑成功",
                type: "success",
              });
            });
          } else {
            createSurvey(this.tableData).then((res) => {
              this.getList();
              this.dialogVisible = false;
              this.$message({
                message: "新增成功",
                type: "success",
              });
            });
          }
        } else {
          return false;
        }
      });
    },
  },
};
</script>
