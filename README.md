# 股票管理系统

<a href="https://github.com/vuejs/vue">
    <img src="https://img.shields.io/badge/vue-2.6.10-brightgreen.svg" alt="vue">
  </a>
  <a href="https://github.com/ElemeFE/element">
    <img src="https://img.shields.io/badge/element--ui-2.8.2-brightgreen.svg" alt="element-ui">
  </a>

基于 Vue + Element UI 的股票系统解决方案。



利用沪市和深市500种股票证券交易数据，在对数据进行了预处理之后，为了更好地理解数据，对数据进行可视化，主要包含以下可视化模块（包含但不限于）：

1. 关注的一只或多只股票16年或17年的走势如何？
2. 哪只或那几只股票的成交量较好？
3. 企业股票在深市或沪市的表现如何？

该系统前端基于 [vue.js](https://cn.vuejs.org/index.html)，使用 vue-cli3 脚手架，引用 Element UI 组件库以及ecahrts组件等核心组件开发，后端采用轻量级Web应用框架[flask](https://flask.palletsprojects.com/en/1.1.x/)，数据库则是采用流行的mysql数据库。

## 功能

-   [x] 登录/注销
-   [x] Dashboard
-   [x] 股票详细信息展示——表单
-   [x] 股票K线图走势分析:sparkles:
-   [x] 股票成交量成交额统计分析 :bar_chart:
-   [ ] 股票信息增删改查
-   [ ] 股票信息成交量对比展示
-   [ ] 股票信息成交额对比展示
-   [ ] 股票信息成交量预测模块

## 系统展示

### 登陆界面

![image-20210101132500720](https://github.com/xjh199923/stockView/tree/master/dataviewWeb/screenshots/login.png)

### 信息展示

![table](https://github.com/xjh199923/stockView/tree/master/dataviewWeb/screenshots/table.png)

## 安装步骤

```sh
git clone https://github.com/lin-xin/vue-manage-system.git      // 把模板下载到本地
cd vue-manage-system    // 进入模板目录
npm install         // 安装项目依赖，等待安装完成之后，安装失败可用 cnpm 或 yarn

// 开启服务器，浏览器访问 http://localhost:8080
npm run serve

// 执行构建命令，生成的dist文件夹放在服务器下即可访问
npm run build
```

## 特别鸣谢

- [vue-manage-system](https://github.com/lin-xin/vue-manage-system)