from flask import Flask, jsonify, request
from models import *
from flask_cors import CORS
from pandas import DataFrame
from predict_dic.predict import *

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
CORS(app, resources=r'/*')

app.config.from_object('config')
db.app = app
db.init_app(app)

db.create_all()

# 返回某一支股票的所有信息
@app.route("/stockInfo/<stockCode>/pageIndex<pageCode>")
def allInfo(stockCode,pageCode):
    pageCode=int(pageCode)-1
    tmplist =[]
    allJson = {}  # 所有信息，包括记录数json
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

# @app.route('/')
# def index():
#     stockMax = Stock.query.all()
#
#
# def add_data(obj):
#     try:
#         db.session.add(obj)
#         db.session.commit()
#     except Exception as e:
#         print(e)
#         db.session.rollback()
#         flash("添加失败")

#返回id当前最大值
@app.route("/curIdmax/")
def curIdmax():
    tmpid = db.session.execute(" SELECT max(id) AS maxID FROM stock ").fetchall()
    tmpdic = {}
    tmplist = []
    for i in tmpid:
        tmplist.append(i.maxID)
    tmpdic['maxId'] = tmplist[0]
    return jsonify(tmpdic)

# 返回某一支股票的交易日期，开盘价，收盘价，最高价，最低价
@app.route("/stock/<stockCode>/")
def allitem(stockCode):
    tmplist = []
    stock = Stock.query.filter_by(stockNumber=stockCode).all()
    for record in stock:
        tmplist.append([record.transactionDate, record.openPrice, record.closePrice,record.highestPrice,record.lowestPrice])
    return jsonify(tmplist)

# 返回某一支股票的成交量，成交额
@app.route("/stockVolume/<stockCode>/")
def stockVolume(stockCode):
    stock = Stock.query.filter_by(stockNumber=stockCode).all()
    records = []
    for record in stock:
        records.append([record.transactionDate, record.volume,record.turnover])
    print(records)
    return jsonify(records)

# 返回股票总数，以及名称列表
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

# 返回深市，沪市分别数目
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

# 返回成交量前n的的股票代码以及成交量信息
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

# 返回某一支股票的2016年2017年股票的成交量
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

#返回深市或者沪市的股票成交量，成交额
@app.route("/boxplot/<stockType>/")
def stockBoxplot(stockType):
    alldata = {}
    allVolume,allTurnover,stockNamelist =  [],[],[]
    global stocksql
    if(stockType == 'sh'):
        stocksql = db.session.execute("SELECT stockName, AVG(stock.volume) AS allVolume FROM stock WHERE stockNumber LIKE '%sz%'\
    GROUP BY stockName,stockName ORDER BY allVolume DESC LIMIT 20").fetchall()
    elif(stockType == 'sz'):
        stocksql = db.session.execute("SELECT stockName, AVG(stock.volume) AS allVolume FROM stock WHERE stockNumber LIKE '%sh%'\
            GROUP BY stockName,stockName ORDER BY allVolume DESC LIMIT 20").fetchall()
    for item in stocksql:
        stockNamelist.append(item.stockName)
    for item1 in stockNamelist:
        stocksql = db.session.execute("SELECT DISTINCT volume,turnover FROM stock\
        WHERE stockName = '%s' " %item1).fetchall()
        tmplist1, tmplist2 = [], []
        for data in stocksql:
            tmplist1.append(data.volume)
            tmplist2.append(data.turnover/30)
        allVolume.append(tmplist1)
        allTurnover.append(tmplist2)
    alldata['allVolume'] = allVolume
    alldata['allTurnover'] = allTurnover
    alldata['stockNamelist'] = stockNamelist
    return jsonify(alldata)

@app.route('/test', methods=['post'])
def test():
    data = request.get_json(silent=True)
    print(data['aid']) #123
    return jsonify(data)

#返回深市或者沪市的股票预测模块
@app.route("/predict/<stockCode>/")
def predic(stockCode):
    stockNumFirstN = db.session.execute("SELECT openPrice,closePrice,highestPrice,lowestPrice,\
        beforeClosePrice,volume,turnover FROM stock WHERE stockNumber = '%s' " %stockCode).fetchall()
    df = DataFrame(stockNumFirstN)
    df.columns = ['openPrice', 'closePrice', 'highestPrice', 'lowestPrice', 'beforeClosePrice', 'volume', 'turnover']
    data = {}

    stocksql = db.session.execute("SELECT transactionDate FROM stock\
            WHERE stockNumber = '%s' " % stockCode).fetchall()
    tmplist = []
    for data1 in stocksql:
        tmplist.append(data1.transactionDate)

    data['origin'] = predic_stock(df)[0].tolist()
    data['predict'] = predic_stock(df)[1].tolist()
    data['date'] = tmplist
    # plt.plot(data['origin'], label='test')
    # plt.plot(data['predict'], label='pred')
    # plt.legend()
    # plt.show()
    return jsonify(data)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.debug = app.config['DEBUG']
    app.run(host="127.0.0.1",
            port=8888,
            debug=True,
            )
