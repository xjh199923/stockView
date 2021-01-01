<template>
    <div class="stockVolume">
        <el-container>
            <el-container style="width:100%;">
                    <el-row :gutter="100">
                        <el-col>
                            <div id="echartContainer" ref="echartContainer" style="width:1000px; height:580px"></div>
                        </el-col>
                    </el-row> 
            </el-container>
            <el-footer>
                <el-row :gutter="10" align="middle">
                    <el-col :span="6">
                        <el-input v-model="codeinput" placeholder="请输入内容"></el-input>
                    </el-col>
                    <el-col :span="6">
                        <el-button type="success" @click="getMessage()">提交code</el-button>
                    </el-col>
                </el-row>
            </el-footer>
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
    };
  },

  methods: {
      getMessage() {
        // 使用 axios 向 flask 发送请求
        var code  = this.codeinput;
        const url = "http://127.0.0.1:8888/stockVolume/"+code;
        console.log(url);
        axios.get(url).then((res) => {
            var colors = ['#5793f3', '#d14a61', '#675bba'];
            var data0 = splitData(res.data);
            console.log(volumeValues(data0)[0]);
            // macd计算
            function splitData(rawData) {
                var categoryData = [];
                var values = [];
                var volumes = [];

                for (var i = 0; i < rawData.length; i++) {
                    categoryData.push(rawData[i].splice(0,1)[0]);
                    values.push(rawData[i])
                }
                return {
                    categoryData: categoryData,
                    values: values
                };
            };
            function volumeValues(data0) {
                var result = [];
                var volumelist = [];
                var turnoverlist = [];
                for (var i = 0, len = data0.values.length; i < len; i++) {
                    volumelist.push(parseFloat(data0.values[i][0])/100);
                    turnoverlist.push(parseFloat(data0.values[i][1])/10000);
                }
                result.push(volumelist);
                result.push(turnoverlist);
                return result;
            };
            var option = {
                color: colors,
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross'
                    }
                },
                grid: {
                    right: '20%'
                },
                toolbox: {
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                legend: {
                    data: ['成交量', '成交额']
                },
                xAxis: [
                    {
                        type: 'category',
                        axisTick: {
                            alignWithLabel: true
                        },
                        data: data0.categoryData,
                        min: 'dataMin',
                        max: 'dataMax'
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        name: '成交量',
                        min: 0,
                        max: 'dataMax',
                        position: 'right',
                        axisLine: {
                            lineStyle: {
                                color: colors[0]
                            }
                        },
                        axisLabel: {
                            formatter: '{value} 10^2'
                        }
                    },
                    {
                        type: 'value',
                        name: '成交额',
                        min: 0,
                        max: 'dataMax',
                        position: 'right',
                        offset:120,
                        axisLine: {
                            lineStyle: {
                                color: colors[1]
                            }
                        },
                        axisLabel: {
                            formatter: '{value} 万元'
                        }
                    }
                ],
                dataZoom: [
                {
                    type: 'inside',
                    start: 90,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    top: '100%',
                    start: 50,
                    end: 100
                }
            ],
                series: [
                    {
                        name: '成交量',
                        type: 'bar',
                        data: volumeValues(data0)[0],
                    },
                    {
                        name: '成交额',
                        type: 'bar',
                        yAxisIndex: 1,
                        data: volumeValues(data0)[1],
                    },
                ]
            };

            var charts = echarts.init(this.$refs.echartContainer);
            charts.setOption(option);
            //this.mes = res.data;
          })
          .catch((error) => {
            console.log(error);
          })
      }
  },
  //在模板渲染成html前调用生命周期函数
  created() {
    this.getMessage();
  },
}
</script>
<style>
    .stockVolume{
        position: absolute;
        left: 50px;
    }
</style>

      