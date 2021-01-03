from flask import Flask,jsonify
from models import *
from flask_cors import CORS
from sqlalchemy import func

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
#返回深市，沪市分别数目
@app.route("/stockNum/")
def stockNum():
    numDic = {}
    nameList = []
    stock = Stock.query.with_entities(Stock.stockNumber).distinct().all()
    for record in stock:
        nameList.append(record.stockNumber)
    szList = [i for i, x in enumerate(nameList) if x.find('sz') != -1]
    numDic['shNum'] = len(nameList) - len(szList)
    numDic['szNum'] = len(szList)
    return jsonify(numDic)

#返回成交量前n的的股票代码以及成交量信息
@app.route("/volumeFirstN/<firstn>/")
def volumeFirstN(firstn):
    tmpNamelist,tmpDatelist,tmpfirstNdata = [],[],[]
    stockNumFirstN = db.session.execute('SELECT stockName, AVG(stock.volume) AS allVolume FROM stock \
    GROUP BY stockName,stockName ORDER BY allVolume DESC LIMIT %s' %firstn).fetchall()
    for record in stockNumFirstN:
        tmpNamelist.append(record.stockName)
    tmpDate = db.session.execute("SELECT transactionDate FROM stock WHERE stockNumber = 'sh600297' ").fetchall()
    for j in tmpDate:
        tmpDatelist.append(j.transactionDate)
    for item in tmpNamelist:
        tmpData = db.session.execute("SELECT transactionDate,volume FROM stock WHERE stockName = '%s' " %item).fetchall()
        tmplist = []
        for i in tmpData:
            tmplist.append(i.volume)
        tmpfirstNdata.append(tmplist)
    firstNdic = {}
    firstNdic['firstNnameList'] = tmpNamelist
    firstNdic['firstNdateList'] = tmpDatelist
    firstNdic['firstNdataList'] = tmpfirstNdata
    return jsonify(firstNdic)

#返回某一支股票的2016年2017年股票的成交量
@app.route("/VolumeContrast16_17/<stockCode>/")
def VolumeContrast16_17(stockCode):
    stock_16 = Stock.query.filter(Stock.stockNumber == stockCode,Stock.transactionDate.like('%2016%')).all()
    stock_17 = Stock.query.filter(Stock.stockNumber == stockCode,Stock.transactionDate.like('%2017%')).all()
    date_16,date_17,volume_16,volume_17 = [],[],[],[]
    alldata = {}
    for record in stock_16:
        date_16.append(record.transactionDate)
        volume_16.append(record.volume)
    for item in stock_17:
        date_17.append(item.transactionDate)
        volume_17.append(item.volume)
    alldata['date_16'] = date_16
    alldata['date_17'] = date_17
    alldata['volume_16'] = volume_16
    alldata['volume_17'] = volume_17
    return jsonify(alldata)



if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.debug = app.config['DEBUG']
    app.run(host="127.0.0.1",
            port=8888,
            debug=True,
            )
