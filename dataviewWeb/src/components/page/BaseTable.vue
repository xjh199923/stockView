<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 股票详情
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-button
                    type="primary"
                    icon="el-icon-delete"
                    class="handle-del mr10"
                    @click="delAllSelection"
                >批量删除</el-button>
                <el-select  v-model="selectCode"
                            clearable
                            filterable
                            @change="getSelectValue()"
                            placeholder="请选择">
                            <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                </el-select>
            </div>
            <el-table
                :data="tableData"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
                @selection-change="handleSelectionChange"
                :default-sort = "{prop: 'stockId', order: 'transactionDate'}"
            >
                <el-table-column type="selection" width="55" align="center"></el-table-column>
                <el-table-column prop="stockId" label="ID" align="center"></el-table-column>
                <el-table-column prop="stockName" label="股票名称" align="center"></el-table-column>
                <el-table-column prop="stockNumber" label="股票代码" width="100" align="center"></el-table-column>
                <el-table-column prop="transactionDate" label="交易日期" width="110" align="center"></el-table-column>
                <el-table-column prop="openPrice" label="开盘价" align="center"></el-table-column>
                <el-table-column prop="closePrice" label="收盘价" align="center"></el-table-column>
                <el-table-column prop="highestPrice" label="最高价" align="center"></el-table-column>
                <el-table-column prop="lowestPrice" label="最低价" align="center"></el-table-column>
                <el-table-column prop="beforeClosePrice" label="前收盘价" align="center"></el-table-column>
                <el-table-column prop="volume" label="成交量" align="center"></el-table-column>
                <el-table-column prop="turnover" label="成交额" align="center"></el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-edit"
                            @click="handleEdit(scope.$index, scope.row)"
                        >编辑</el-button>
                        <el-button
                            type="text"
                            icon="el-icon-delete"
                            class="red"
                            @click="handleDelete(scope.$index, scope.row)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination
                    background
                    layout="total, prev, pager, next"
                    :current-page="query.pageIndex"
                    :page-size="query.pageSize"
                    :total="pageTotal"
                    @current-change="handlePageChange"
                ></el-pagination>
            </div>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
            <el-form ref="form" :model="form" label-width="70px">
                <el-form-item label="用户名">
                    <el-input v-model="form.name"></el-input>
                </el-form-item>
                <el-form-item label="地址">
                    <el-input v-model="form.address"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'basetable',
    data() {
        return {
            query: {
                address: '上海股票',
                pageIndex: 1,
                pageSize: 10
            },
            stockCode: 'sh600297',
            tableData: [],
            multipleSelection: [],
            delList: [],
            editVisible: false,
            pageTotal: 10,
            form: {},
            idx: -1,
            id: -1,
            options: '',
            selectCode: ''
        };
    },
    created() {
        this.getVolumes();
        this.getData();
    },
    methods: {
        getData() {
            var code  = this.stockCode;
            // 获取 easy-mock 的模拟数据
            const url = "http://127.0.0.1:8888/stockInfo/"+code+"/pageIndex"+this.query.pageIndex;
            axios.get(url).then((res) => {
                this.tableData = res.data.infoList;
                console.log(res.data.infoList)
                this.pageTotal = res.data.infoLen;
            });
        },
        getVolumes(){
          // 使用 axios 向 flask 发送请求/curIdmax
          const url = "http://127.0.0.1:8888/stockName/";
          console.log(url);
          var tplist = [];
          axios.get(url).then((res) => {
              for (var i = 0, len = res.data.nameList.length; i < len; i++) {
                  var tmpdic = [];
                  tmpdic['value'] = i;
                  tmpdic['label'] = res.data.nameList[i];
                  tplist.push(tmpdic);
              }
              this.options = tplist;
          })
          .catch((error) => {
              console.log(error);
          })
        },
        //得到select选框当前选中
        getSelectValue(value){
            this.stockCode = this.options[this.selectCode].label;
            this.query.pageIndex = 1;
            this.getData();
        },
        // 删除操作
        handleDelete(index, row) {
            // 二次确认删除
            this.$confirm('确定要删除吗？', '提示', {
                type: 'warning'
            })
                .then(() => {
                    this.$message.success('删除成功');
                    this.tableData.splice(index, 1);
                })
                .catch(() => {});
        },
        // 多选操作
        handleSelectionChange(val) {
            this.multipleSelection = val;
        },
        delAllSelection() {
            const length = this.multipleSelection.length;
            let str = '';
            this.delList = this.delList.concat(this.multipleSelection);
            for (let i = 0; i < length; i++) {
                str += this.multipleSelection[i].name + ' ';
            }
            this.$message.error(`删除了${str}`);
            this.multipleSelection = [];
        },
        // 编辑操作
        handleEdit(index, row) {
            this.idx = index;
            this.form = row;
            this.editVisible = true;
        },
        // 保存编辑
        saveEdit() {
            this.editVisible = false;
            this.$message.success(`修改第 ${this.idx + 1} 行成功`);
            this.$set(this.tableData, this.idx, this.form);
        },
        // 分页导航
        handlePageChange(val) {
            this.$set(this.query, 'pageIndex', val);
            this.getData();
        }
    }
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
</style>
