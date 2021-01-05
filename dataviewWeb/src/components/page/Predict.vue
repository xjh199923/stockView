<template>
    <div class="stockVolume">
        <el-container>
            <el-container style="width:100%;">
                    <el-row :gutter="100">
                        <el-col :span="18">
                            <div id="echartPredict" ref="echartPredict"style="width:1000px; height:580px"></div>
                        </el-col>
                        <el-col :span="6">
                            <el-table
                                ref="stockNameTable" 
                                :data="tableData"
                                height="550"
                                fixed
                                size='mini'
                                highlight-current-row
                                style="width: 170px"
                                :default-sort = "{prop: 'stockName', order: 'ascending'}">
                                <el-table-column
                                prop="stockName"
                                label="股票代码"
                                align="center"
                                width="160"
                                sortable
                                >
                                    <template slot-scope="scope">
                                        <el-button type="text" @click="checkDetail(scope.row)">{{scope.row.stockName}}</el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-col>
                    </el-row> 
            </el-container>
        </el-container>
    </div>
    
</template>

<script>
import axios from 'axios'
var echarts = require("echarts");
export default {
  data() {
    return {
        codeinput: "sh600297",
        data: "",
        tableData: [{
          stockName: 'sh600297',
        }]
    };
  },
  methods: {
      getstockAllnumber(){
        const url = "/stockName/";
        axios.get(url).then((res) => {
            var vars = [];
            for(var i=0;i<res.data.nameList.length;i++)
            {
                let tmpdic = { stockName: res.data.nameList[i]};
                vars.push(tmpdic)
            }
            this.tableData = vars;
          })
          .catch((error) => {
            console.log(error);
          })
      },
      checkDetail(val){
        this.codeinput = val.stockName;
        this.getMessage();
      },
      getMessage(id) {
        // 使用 axios 向 flask 发送请求
        var code  = this.codeinput;
        const url = "/predict/"+code;
        axios.get(url).then((res) => {
            var date = res.data.date;
            var origin = res.data.origin;
            var predict  = res.data.predict;

            var colors = ['#d14a61', '#675bba'];
            var option = {
                color: colors,

                tooltip: {
                    trigger: 'none',
                    axisPointer: {
                        type: 'cross'
                    }
                },
                legend: {
                    data:['成交额', '成交额预测']
                },
                grid: {
                    top: 70,
                    bottom: 50
                },
                toolbox: {
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                xAxis: [
                    {
                        type: 'category',
                        axisTick: {
                            alignWithLabel: true
                        },
                        axisLine: {
                            onZero: false,
                            lineStyle: {
                                color: colors[1]
                            }
                        },
                        axisPointer: {
                            label: {
                                formatter: function (params) {
                                    return '成交额预测  ' + params.value
                                        + (params.seriesData.length ? '：' + params.seriesData[0].data : '');
                                }
                            }
                        },
                        data: date
                    },
                    {
                        type: 'category',
                        axisTick: {
                            alignWithLabel: true
                        },
                        axisLine: {
                            onZero: false,
                            lineStyle: {
                                color: colors[0]
                            }
                        },
                        axisPointer: {
                            label: {
                                formatter: function (params) {
                                    return '成交额  ' + params.value
                                        + (params.seriesData.length ? '：' + params.seriesData[0].data : '');
                                }
                            }
                        },
                        data: date
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value}'
                        }
                    }
                ],
                dataZoom: [
                {
                    type: 'inside',
                    xAxisIndex: [0,1],
                    start: 30,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    top: '100%',
                    start: 50,
                    end: 100
                }],
                series: [
                    {
                        name: '成交额',
                        type: 'line',
                        xAxisIndex: 1,
                        smooth: true,
                        data: origin
                    },
                    {
                        name: '成交额预测',
                        type: 'line',
                        smooth: true,
                        data: predict
                    }
                ]
            };
            var charts = echarts.init(this.$refs.echartPredict);
            if (option && typeof option === "object") {
                charts.setOption(option, true);
            }
          })
          .catch((error) => {
            console.log(error);
          })
      }
  },
  //在模板渲染成html前调用生命周期函数
  created() {
    this.getMessage();
    this.getstockAllnumber();
  },
}
</script>
<style>
    .stockVolume{
        position: absolute;
        left: 50px;
    }
</style>

      