<template>
    <div class="stockVolume">
        <el-container>
            <el-container style="width:100%;">
                    <el-row :gutter="100">
                        <el-col :span="18">
                            <div id="echart16_17" ref="echart16_17"style="width:1000px; height:580px"></div>
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
        const url = "http://127.0.0.1:8888/stockName/";
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
        console.log(val.stockName)
        this.codeinput = val.stockName;
        this.getMessage();
      },
      getMessage(id) {
        // 使用 axios 向 flask 发送请求
        var code  = this.codeinput;
        const url = "http://127.0.0.1:8888/VolumeContrast16_17/"+code;
        axios.get(url).then((res) => {
            var date_16 = res.data.date_16;
            var date_17 = res.data.date_17;
            var volume_16 = res.data.volume_16;
            var volume_17  = res.data.volume_17;

            // var dom = document.getElementById(id);
            var colors = ['#5793f3', '#d14a61', '#675bba'];
            var option = {
                color: colors,

                tooltip: {
                    trigger: 'none',
                    axisPointer: {
                        type: 'cross'
                    }
                },
                legend: {
                    data:['2016 成交量', '2017 成交量']
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
                                    return '成交量  ' + params.value
                                        + (params.seriesData.length ? '：' + params.seriesData[0].data : '');
                                }
                            }
                        },
                        data: date_16
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
                                    return '成交量  ' + params.value
                                        + (params.seriesData.length ? '：' + params.seriesData[0].data : '');
                                }
                            }
                        },
                        data: date_17
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value} 元'
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
                        name: '2016 成交量',
                        type: 'line',
                        xAxisIndex: 1,
                        smooth: true,
                        data: volume_16
                    },
                    {
                        name: '2017 成交量',
                        type: 'line',
                        smooth: true,
                        data: volume_17
                    }
                ]
            };
            var charts = echarts.init(this.$refs.echart16_17);
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

      