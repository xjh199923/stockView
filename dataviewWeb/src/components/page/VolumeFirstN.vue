<template>
    <div class="stockVolume">
        <el-container>
            <el-container style="width:100%;">
                    <el-row :gutter="100">
                        <el-col>
                            <div id="echartContainer" ref="echartContainer" style="width:1200px; height:580px"></div>
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
    };
  },

  methods: {
      getMessage() {
        // 使用 axios 向 flask 发送请求
        const url = "/volumeFirstN/5";
        axios.get(url).then((res) => {
                
                var tmpNamelist = res.data.firstNnameList;
                var tmpDatelist = res.data.firstNdateList;
                var tmpfirstNdata = res.data.firstNdataList;

                var seriseData = []
                for(let i = 0; i < tmpNamelist.length; i++){
                    let tmpdic = { 
                        name: tmpNamelist[i],
                        type: 'line',
                        data: tmpfirstNdata[i]
                    };
                    seriseData.push(tmpdic);
                }

                var colors = ['#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074', '#546570', '#c4ccd3'];
                var option = {
                title: {
                    text: '成交量排名前N支股票',
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: tmpNamelist
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                dataZoom: [
                {
                    type: 'inside',
                    start: 30,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    top: '100%',
                    start: 30,
                    end: 100
                }
                ],
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: tmpDatelist
                },
                yAxis: {
                    type: 'value'
                },
                // color: colors,
                series: seriseData
            };       
            var charts = echarts.init(this.$refs.echartContainer);
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
</style>

      