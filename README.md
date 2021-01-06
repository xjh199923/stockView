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
-   [x] 股票信息增删改查
-   [x] 股票信息成交量2016&2017年对比分析功能
-   [x] 成交量排名前N支股票对比分析
-   [x] 股票信息成交量&成交额的平稳性分析
-   [x] 基于全连接神经网络股票信息成交额预测模块

## 系统展示

### 登陆界面

![login](./dataviewWeb/screenshots/login.png)

### 系统首页

![login](./dataviewWeb/screenshots/homePage.png)

### 股票详细信息展示

![login](./dataviewWeb/screenshots/stockDetails.png)

### 股票K线图展示

![login](./dataviewWeb/screenshots/k_line.png)

### 股票成交量成交额对比展示

![login](./dataviewWeb/screenshots/turnoverVolumeContrast.png)

### 股票成交量16-17年对比分析

![login](./dataviewWeb/screenshots/16——17.png)

### 成交量TOPN展示

![login](./dataviewWeb/screenshots/topN.png)

### 股票平稳性分析

![login](./dataviewWeb/screenshots/stabilityAnalysis.png)

### 神经网络预测结果展示

![login](./dataviewWeb/screenshots/predict.png)



## 安装步骤

### clone项目

```sh
git clone https://github.com/xjh199923/stockView.git   // 把项目下载到本地
cd stockView   // 进入项目
```

### 后端项目安装

#### 数据库配置

将后端backFlask目录文件夹，导入的你的python环境下，之后需要在本地建立名为`stockDatabase`的mysql数据库，并修改config.py中的数据库配置如下：

```python
# 配置 sqlalchemy  "数据库驱动://数据库用户名:@主机地址:端口/数据库名称"
SQLALCHEMY_DATABASE_URI = "mysql://数据库用户名:password@localhost:3306/stockDatabase"
```

#### Flask环境配置：

Python依赖如下：

```
absl-py==0.11.0
astor==0.8.1
cached-property==1.5.2
certifi==2020.12.5
click==7.1.2
cycler==0.10.0
Flask==1.1.2
Flask-Cors==3.0.9
Flask-SQLAlchemy==2.4.4
gast==0.4.0
grpcio==1.34.0
h5py==3.1.0
importlib-metadata==3.3.0
itsdangerous==1.1.0
Jinja2==2.11.2
joblib==1.0.0
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.2
kiwisolver==1.3.1
Markdown==3.3.3
MarkupSafe==1.1.1
matplotlib==3.3.3
mock==4.0.3
numpy==1.19.4
pandas==1.2.0
Pillow==8.1.0
protobuf==3.14.0
PyMySQL==0.10.1
pyparsing==2.4.7
python-dateutil==2.8.1
pytz==2020.5
scikit-learn==0.24.0
scipy==1.6.0
six==1.15.0
sklearn==0.0
SQLAlchemy==1.3.22
tensorboard==1.13.1
tensorflow==1.13.2
tensorflow-estimator==1.13.0
termcolor==1.1.0
threadpoolctl==2.1.0
typing-extensions==3.7.4.3
Werkzeug==1.0.1
zipp==3.4.0
```

可以利用以下命令安装：

```shell
pip install -r requirements.txt
```

依赖安装完成后，运行FlaskDemo.py即可启动后端服务器。

### 前端项目安装

```shell
cd  dataviewWeb  //进入前端项目目录 

npm install         // 安装项目依赖，等待安装完成之后，安装失败可用 cnpm 或 yarn

// 开启服务器，浏览器访问 http://localhost:8080
npm run serve

// 执行构建命令，生成的dist文件夹放在服务器下即可访问
npm run build
```

### 数据配置文件

预处理过后的数据以SQL的格式进行保存，mysql运行即可生成相应的数据库。

## 特别鸣谢

- [vue-manage-system](https://github.com/lin-xin/vue-manage-system)