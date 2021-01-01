from database import db

#股票数据库设计
class Stock(db.Model):
    #Columns
    __tablename = 'Stock'

    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    stockNumber = db.Column(db.String(10))
    stockName = db.Column(db.String(20))
    transactionDate = db.Column(db.String(20))
    openPrice = db.Column(db.Float)
    closePrice = db.Column(db.Float)
    highestPrice = db.Column(db.Float)
    lowestPrice = db.Column(db.Float)
    beforeClosePrice = db.Column(db.Float)
    volume = db.Column(db.Float)
    turnover = db.Column(db.Float)

    def __init__(self,id, stockNumber,stockName,transactionDate,openPrice,
        closePrice,highestPrice,lowestPrice,beforeClosePrice,volume,turnover):
        self.id = id
        self.stockNumber = stockNumber
        self.stockName = stockName
        self.transactionDate = transactionDate
        self.openPrice = openPrice
        self.closePrice = closePrice
        self.highestPrice = highestPrice
        self.lowestPrice = lowestPrice
        self.beforeClosePrice = beforeClosePrice
        self.volume = volume
        self.turnover = turnover
