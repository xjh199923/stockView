<template>
    <div class="kline_div">
        <el-container>
            <el-container style="width:100%;">
                    <el-row :gutter="100">
                        <el-col :span="18">
                            <div id="echartContainer" ref="echartContainer"  style="width:1000px; height:700px"></div>
                        </el-col>
                        <el-col :span="6">
                            <br>
                            <el-row>
                                <el-select popper-class="el_selectcode"
                                           v-model="selectCode"
                                           @change="getSelectValue()"
                                           clearable
                                           filterable
                                           placeholder="请选择"
                                           style="height: 600px">
                                    <el-option
                                      v-for="item in options"
                                      :key="item.value"
                                      :label="item.label"
                                      :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-row>

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
        data: "",
        code: 'sh600297',
        options: '',
        selectCode: ''
    };
  },

  methods: {
      getMessage() {
        // 使用 axios 向 flask 发送请求
        var code  = this.code;
        const url = "http://127.0.0.1:8888/stock/"+code;
        console.log(url);
        axios.get(url).then((res) => {
            var data0 = splitData(res.data);
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
            function calculateMA(dayCount) {
                var result = [];
                for (var i = 0, len = data0.values.length; i < len; i++) {
                    if (i < dayCount) {
                        result.push('-');
                        continue;
                    }
                    var sum = 0;
                    for (var j = 0; j < dayCount; j++) {
                        sum += parseFloat(data0.values[i - j][1]);
                    }
                    result.push(sum / dayCount);
                }
                return result;
            };
            var option = {
            title: {
                text: this.codeinput
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                }
            },
            legend: {
                data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
            },
            grid: {
                left: '10%',
                right: '10%',
                bottom: '15%'
            },
            xAxis: {
                type: 'category',
                data: data0.categoryData,
                scale: true,
                boundaryGap: false,
                axisLine: {onZero: false},
                splitLine: {show: false},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax'
            },
            yAxis: {
                    scale: true,
                    splitArea: {
                        show: true
                    }
                },
            dataZoom: [
                {
                    type: 'inside',
                    start: 70,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    top: '90%',
                    start: 70,
                    end: 100
                }
            ],
            series: [
                {
                    name: '日K',
                    type: 'candlestick',
                    data: data0.values,
                    itemStyle: {
                        color: '#ec0000',
                        color0: '#00da3c',
                        borderColor: '#8A0000',
                        borderColor0: '#008F28'
                    },
                    markPoint: {
                        label: {
                            normal: {
                                formatter: function (param) {
                                    return param != null ? Math.round(param.value) : '';
                                }
                            }
                        },
                        data: [
                            {
                                name: 'XX标点',
                                coord: ['2013/5/31', 2300],
                                value: 2300,
                                itemStyle: {
                                    color: 'rgb(41,60,85)'
                                }
                            },
                            {
                                name: 'highest value',
                                type: 'max',
                                valueDim: 'highest'
                            },
                            {
                                name: 'lowest value',
                                type: 'min',
                                valueDim: 'lowest'
                            },
                            {
                                name: 'average value on close',
                                type: 'average',
                                valueDim: 'close'
                            }
                        ],
                        tooltip: {
                            formatter: function (param) {
                                return param.name + '<br>' + (param.data.coord || '');
                            }
                        }
                    },
                    markLine: {
                        symbol: ['none', 'none'],
                        data: [
                            [
                                {
                                    name: 'from lowest to highest',
                                    type: 'min',
                                    valueDim: 'lowest',
                                    symbol: 'circle',
                                    symbolSize: 10,
                                    label: {
                                        show: false
                                    },
                                    emphasis: {
                                        label: {
                                            show: false
                                        }
                                    }
                                },
                                {
                                    type: 'max',
                                    valueDim: 'highest',
                                    symbol: 'circle',
                                    symbolSize: 10,
                                    label: {
                                        show: false
                                    },
                                    emphasis: {
                                        label: {
                                            show: false
                                        }
                                    }
                                }
                            ],
                            {
                                name: 'min line on close',
                                type: 'min',
                                valueDim: 'close'
                            },
                            {
                                name: 'max line on close',
                                type: 'max',
                                valueDim: 'close'
                            }
                        ]
                    }
                },
                {
                    name: 'MA5',
                    type: 'line',
                    data: calculateMA(5),
                    smooth: true,
                    lineStyle: {
                        opacity: 0.5
                    }
                },
                {
                    name: 'MA10',
                    type: 'line',
                    data: calculateMA(10),
                    smooth: true,
                    lineStyle: {
                        opacity: 0.5
                    }
                },
                {
                    name: 'MA20',
                    type: 'line',
                    data: calculateMA(20),
                    smooth: true,
                    lineStyle: {
                        opacity: 0.5
                    }
                },
                {
                    name: 'MA30',
                    type: 'line',
                    data: calculateMA(30),
                    smooth: true,
                    lineStyle: {
                        opacity: 0.5
                    }
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
      },
      getVolumes(){
          // 使用 axios 向 flask 发送请求
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
          this.code = this.options[this.selectCode].label;
          this.getMessage();
      }
  },

  //在模板渲染成html前调用生命周期函数
  created() {
      this.getVolumes();
      this.getMessage();
  }
}
</script>
<style>
    .el-table{
        background-color: Transparent;
        line-height: 60px;
    }
    .kline_div{
        position: absolute;
        left: 50px;
    }
</style>

      