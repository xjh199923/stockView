<template>
    <div class="stockVolume">
        <el-container>
            <el-header>
                <el-row :gutter="20" class="mgb20">
                    <el-col :span="10">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-1">
                                <i class="el-icon-s-fold grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">深市</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="4">
                        <el-button type="primary" size='medium' style="position:relative;left:40px;top:20px" @click="changeType()">
                            切换股市
                        </el-button>
                    </el-col>
                    <el-col :span="10">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-2">
                                <i class="el-icon-s-unfold grid-con-icon" style="position:relative;left:390px;top:0px"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num" style="position:relative;right:80px;top:0px">沪市</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </el-header>
            <el-main><div id="echartBox" ref="echartBox" style="width:1200px; height:580px"></div></el-main>
        </el-container>
    </div>
    
</template>

<script>
import axios from 'axios'
var echarts = require("echarts");
import dataTool  from 'echarts/extension/dataTool'
export default {
  data() {
    return {
        data: "",
        type: false,
        stockType : 'sh'
    };
  },

  methods: {
      changeType(){
          this.stockType = 'sz';
          this.getMessage();
      },
      getMessage() {
        // 使用 axios 向 flask 发送请求
        const url = "/boxplot/"+this.stockType;
        axios.get(url).then((res) => {

                var tmpNamelist = res.data.stockNamelist;
                var tmpVolumelist = res.data.allVolume;
                var tmpallTurnoverlist = res.data.allTurnover;
                var data = echarts.dataTool.prepareBoxplotData(tmpVolumelist);
                var data1 = echarts.dataTool.prepareBoxplotData(tmpallTurnoverlist);
                var colors = ['#5793f3', '#d14a61', '#675bba'];
                var option = {
                        title: {
                            text: '成交量&成交额稳定性分析',
                            left: 'center',
                        },
                        legend: {
                            top: '10%',
                            data: ['成交量', '成交额']
                        },
                        tooltip: {
                            trigger: 'item',
                            axisPointer: {
                                type: 'shadow'
                            }
                        },
                        grid: {
                            left: '10%',
                            top: '20%',
                            right: '10%',
                            bottom: '15%'
                        },
                        xAxis: {
                            type: 'category',
                            data: tmpNamelist,
                            boundaryGap: true,
                            nameGap: 30,
                            splitArea: {
                                show: true
                            },
                            axisLabel: {
                                formatter: '{value}'
                            },
                            splitLine: {
                                show: false
                            }
                        },
                        yAxis: {
                            type: 'value',
                            name: 'Value',
                            min: -4000000,
                            max: 'dataMax',
                            splitArea: {
                                show: false
                            }
                        },
                        dataZoom: [
                            {
                                type: 'inside',
                                start: 0,
                                end: 20
                            },
                            {
                                show: true,
                                height: 20,
                                type: 'slider',
                                top: '90%',
                                xAxisIndex: [0],
                                start: 0,
                                end: 20
                            }
                        ],
                        series: [
                            {
                                name: '成交量',
                                type: 'boxplot',
                                data: data.boxData,
                                tooltip: {formatter: formatter}
                            },
                            // {
                            //     name: 'outlier1',
                            //     type: 'scatter',
                            //     data: data1.outliers
                            // },
                             {
                                name: '成交额',
                                type: 'boxplot',
                                data: data1.boxData,
                                tooltip: {formatter: formatter1}
                            },
                            // {
                            //     name: 'outlier',
                            //     type: 'scatter',
                            //     data: data.outliers
                            // },
                        ]
                    };

                    function formatter(param) {
                        return [
                            param.name + ': ',
                            'upper: ' + param.data[0],
                            'Q1: ' + param.data[1],
                            'median: ' + param.data[2],
                            'Q3: ' + param.data[3],
                            'lower: ' + param.data[4]
                        ].join('<br/>');
                    };
                    function formatter1(param) {
                        return [
                            param.name + ': ',
                            'upper: ' + param.data[0]+'*100 ¥',
                            'Q1: ' + param.data[1]+'*100 ¥',
                            'median: ' + param.data[2]+'*100 ¥',
                            'Q3: ' + param.data[3]+'*100 ¥',
                            'lower: ' + param.data[4]+'*100 ¥'
                        ].join('<br/>');
                    };

            var charts = echarts.init(this.$refs.echartBox);
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
  },
}
</script>
<style>
.stockVolume{
        position: absolute;
        left: 50px;
    }
.el-row {
    margin-bottom: 20px;
}

.grid-content {
    display: flex;
    align-items: center;
    height: 70px;
}

.grid-cont-right {
    flex: 1;
    text-align: center;
    font-size: 14px;
    color: #999;
}

.grid-num {
    font-size: 30px;
    font-weight: bold;
}

.grid-con-icon {
    font-size: 50px;
    width: 100px;
    height: 100px;
    text-align: center;
    line-height: 100px;
    color: #fff;
}

.grid-con-1 .grid-con-icon {
    background: rgb(45, 140, 240);
    text-align: center;
}

.grid-con-1 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
    background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-icon3 {
    font-size: 50px;
    width: 100px;
    height: 50px;
    text-align: center;
    line-height: 100px;
    color: #fff;
}

</style>


      