from datetime import datetime
from app import db

class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

class info(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False) # 图片名
    image = db.Column(db.String(300)) # 图片结果
    number =  db.Column(db.String(100)) # 小麦穗数
    remarks = db.Column(db.String(300)) # 备注
    Conf_thres =  db.Column(db.String(300)) 
    AIDetector_pytorch =  db.Column(db.String(300)) 
    createtime = db.Column(db.DateTime, default=datetime.now) # 建卡时间


