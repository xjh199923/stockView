from flask import Flask,jsonify
from models import *
from flask_cors import CORS

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
CORS(app, resources=r'/*')

app.config.from_object('config')
db.app = app
db.init_app(app)

db.create_all()

#返回某一支股票的所有信息
@app.route("/stockInfo/<stockCode>/pageIndex<pageCode>")
def allInfo(stockCode,pageCode):
    pageCode=int(pageCode)-1
    tmplist =[]
    allJson = {} #所有信息，包括记录数json
    stockInfo = Stock.query.filter_by(stockNumber=stockCode).all()
    stockId = 1
    for record in stockInfo:
        stockDic = {}
        stockDic['stockId'] = record.id
        stockDic["stockName"] = record.stockName
        stockDic["stockNumber"] = record.stockNumber
        stockDic["transactionDate"] = record.transactionDate
        stockDic["openPrice"] = record.openPrice
        stockDic["closePrice"] = record.closePrice
        stockDic["highestPrice"] = record.highestPrice
        stockDic["lowestPrice"] = record.lowestPrice
        stockDic["beforeClosePrice"] = record.beforeClosePrice
        stockDic["volume"] = record.volume
        stockDic["turnover"] = record.turnover
        stockId += 1
        tmplist.append(stockDic)
    allJson["infoLen"] = len(tmplist)
    allJson["infoList"] = tmplist[10*pageCode:10*(pageCode+1)]
    return jsonify(allJson)

#返回某一支股票的交易日期，开盘价，收盘价，最高价，最低价
@app.route("/stock/<stockCode>/")
def allitem(stockCode):
    tmplist = []
    stock = Stock.query.filter_by(stockNumber=stockCode).all()
    for record in stock:
        tmplist.append([record.transactionDate, record.openPrice, record.closePrice,record.highestPrice,record.lowestPrice])
    return jsonify(tmplist)

#返回某一支股票的成交量，成交额
@app.route("/stockVolume/<stockCode>/")
def stockVolume(stockCode):
    stock = Stock.query.filter_by(stockNumber=stockCode).all()
    records = []
    for record in stock:
        records.append([record.transactionDate, record.volume,record.turnover])
    print(records)
    return jsonify(records)

#返回股票总数，以及名称列表
@app.route("/stockName/")
def stockName():
    nameList = []
    nameDic = {}
    stock = Stock.query.with_entities(Stock.stockNumber).distinct().all()
    for record in stock:
        nameList.append(record.stockNumber)
    nameDic['nameList'] = list(set(nameList))
    nameDic['nameLen'] = len(nameList)
    return jsonify(nameDic)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.debug = app.config['DEBUG']
    app.run(host="127.0.0.1",
            port=8888,
            debug=True,
            )
