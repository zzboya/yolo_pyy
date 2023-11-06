from __future__ import print_function
import sys
from flask import Blueprint,jsonify,redirect, url_for, request,session
from config import Config
from app import db
from app.Model.models import user

# Configure Blueprint.
authentication_blueprint = Blueprint(
    'authentication', __name__, url_prefix='/')
authentication_blueprint.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

def md5(user):
    """对用户token进行加密"""
    import hashlib
    import time

    ctime = str(time.time())
    m = hashlib.md5(bytes(str(user), encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()

@authentication_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        try:
            u = user(username=data.get("username"), 
                    password=data.get("password"),
                    email=data.get("email"),
                    phone=data.get("phone"),
                    )
            db.session.add(u)
            db.session.commit()
            rsp={
                "msg": "注册成功",
            }
            return jsonify(rsp)
        except Exception as e:
            rsp={
                "msg": e,
            }
            return jsonify(rsp)

@authentication_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        user_ = user.query.filter_by(username=username).first()
        
        if user_.password == password:
            session.clear()
            session['user_name'] = user_.username
            rsp = { 
                "auth_token" : md5(user_),
                'username':user_.username,
            }
            return jsonify(rsp)
    except Exception as e:
        print(e)
        rsp = { 
            "msg" : e,
        }
        return jsonify(rsp)

@authentication_blueprint.route('/profile/', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        try:
            username = session.get('user_name') 
            username_ = request.args.get("username")
            if username == username_:
                user_ = user.query.filter_by(username=username).first()
                rsp = { 
                "username" : user_.username,
                "email" : user_.email,
                "phone" : user_.phone,
                }
                return jsonify(rsp)
            else:
                rsp = { 
                "msg" : "error",
                }
                return jsonify(rsp)
        except Exception as e:
            print(e)
            rsp = { 
                "msg" : e,
            }
            return jsonify(rsp)
    if request.method == "POST":
        try:
            username_ = request.json.get("username")
            password_ = request.json.get("password")
            email_ = request.json.get("email")
            phone_ = request.json.get("phone")
            newpassword_ = request.json.get("newpassword")
            print("New password,", request.json)
            user_ = user.query.filter_by(username=username_).first()
            if user_.password == password_:
                print("test")
                user_.email = email_
                user_.phone = phone_
                user_.password = newpassword_
                db.session.commit()
                rsp = { 
                "msg" : "success",
                }
                return jsonify(rsp)
            else:
                rsp={
                    "msg":"输入的密码有误",
                }
                return jsonify(rsp)
        except Exception as e:
            print(e)
            rsp={
                    "msg":"字段有重复，请核实相应字段",
                }
            return jsonify(rsp)



import functools
def auth(func):
    @functools.wraps(func)
    def inner(*args,**kwargs):
        # 获取创建的session
        username = session.get('user_name') 
        # 如果不存在session 重定向跳转至登陆页面
        if not username:
            return redirect(url_for('authentication.login'))
 
        return func(*args,**kwargs)
    return inner
