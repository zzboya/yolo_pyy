from __future__ import print_function
import cv2
import core.main
from processor.AIDetector_pytorch import Detector
from processor.ALL import detect_big_image
from datetime import datetime
import math
import os
import json
import sys
import base64
from flask import Blueprint, jsonify, request
from config import Config
from app import db
from app.Model.models import info
import processor.ALL
from flask_paginate import Pagination, get_page_parameter

from processor.crop_overlap_solo import split_image
import processor.detect
from processor.yolo2voc import conver_labels
from processor.demo1 import big_detect
from processor.quemiaobig import big_miss

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER  # '..\\View\\templates'
imgdir = Config.STATIC_FOLDER
# import sys
# # 添加 crop_overlap_solo.py 所在的目录
# sys.path.append('E:/model/web/backend-flask/processor')


# 维护此处的模型， key为前端显示的名字，value为模型路径
weights_dict = {
    # "final":r"weights\final.pt",
    "last": r"weights\last.pt",
    "yolov5": r"weights\yolov5m.pt",
}

# BASE_DIR = os.path.dirname(__file__)


@bp_routes.route('/test/', methods=['GET', 'POST'])
def test():

    imgs = cv2.imread(
        r"D:\william\tempworkfold\yolo\modify\backend-flask\imgs\2023-04-24_20_06_47.jpg")
    dtc = Detector()
    im, image_info = dtc.detect(imgs)
    cv2.imwrite('./tmp/draw/{}.{}'.format("file_name", "jpg"), im)
    print(im, image_info)


@bp_routes.route('/imgprocess/', methods=['GET', 'POST'])
def imgprocess():
    if request.method == 'GET':
        weights_dict_list = list(weights_dict.keys())
        rsp = {
            "weights_dict_list": weights_dict_list,
        }
        return jsonify(rsp)

    if request.method == 'POST':
        data = request.form
        file = request.files

        # 获取请求参数
        Conf_thres = data.get('Conf_thres')
        remarks = data.get('remarks')
        AIDetector_pytorch = data.get('AIDetector_pytorch')
        data_file = request.files.get("data_file")
        # datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"."+data_file.filename.split('.')[-1]
        file_name = data_file.filename
        print('imgdir'+imgdir+'filename'+file_name)
        # 保存上传的图片文件
        oriname = imgdir+file_name  # 原始
        print("oriname,", oriname)
        data_file.save(oriname)
        print(
            " data_file.filename.rsplit('.', 1)[1],", data_file.filename.rsplit('.', 1)[1])

        print('filename::'+file_name.split('.')[0])
        result, miss_count, output_path = detect_big_image(
            file_name.split('.')[0], Conf_thres)
        print(result, miss_count, output_path)
        # 调用 AI 检测函数进行处理
        # pid, image_info =  core.main.c_main(
        #   oriname, Detector(threshold= float(Conf_thres),model=weights_dict[AIDetector_pytorch]),  data_file.filename.rsplit('.', 1)[1])

        # 保存检测结果图片
        resname = output_path  # "./tmp/draw/"+file_name#pid  #结果
        # num = len(image_info)
        # tableData=[]
        # for key,value in image_info.items():
        #     tmp={}
        #     tmp["type"]=key
        #     tmp["size"]=value[0]
        #     tmp["confidence"]=value[1]
        #     tableData.append(tmp)

        # 保存数据到数据库
        # u = info( name = file_name,
        #             image= resname ,
        #             number = num ,
        #             remarks = remarks,
        #             #AIDetector_pytorch=AIDetector_pytorch,
        #             #Conf_thres=Conf_thres,
        #             )
        # db.session.add(u)
        # db.session.commit()

        # 将图片转为 Base64 编码
        with open(resname, "rb") as f:
            result_img = f.read()
            result_img = base64.b64encode(result_img).decode()
            result_img = result_img
        with open(oriname, "rb") as f:
            original_img = f.read()
            original_img = base64.b64encode(original_img).decode()
            original_img = original_img

        # 组装返回结果
        rsp = {
            'status': 1,
            "original_img": "data:image/jpeg;base64,"+original_img,
            "result_img": "data:image/jpeg;base64,"+result_img,
            "seedlingCount": result[0],
            "weedCount": result[1],
            "missingCount": miss_count,
            # 'image_info': tableData,
            "num": 100,
        }
        return jsonify(rsp)


@bp_routes.route('/get_data_list/', methods=['GET', 'POST'])
def get_data_list():
    if request.method == 'GET':
        # data = recent_hot.query.all()
        # 分页查询所有的数据  组装数据
        pageSize = int(request.args.get('size'))
        # 获取页码 默认为1 int类型
        page = int(request.args.get('page'))
        start = (page - 1) * pageSize       # limit后第一个参数 每一页开始位置
        end = start + pageSize              # limit后第二个参数 每一页结束位置

        total = info.query.count()  # 总记录数
        data = info.query.slice(start, end)
        data_list = []
        for i in data:
            with open(i.image, "rb") as f:
                result_img = f.read()
                result_img = base64.b64encode(result_img).decode()
                result_img = result_img
            tmp = {
                "id": i.id,
                "name": i.name,
                "image": "data:image/jpeg;base64,"+result_img,
                "number": i.number,
                "remarks": i.remarks,
                "createtime": i.createtime.strftime('%Y-%m-%d %H:%M:%S'),
            }
            data_list.append(tmp)
        totalPage = total / \
            pageSize if total % pageSize == 0 else (total / pageSize) + 1
        pageInfo = {"nowPage": page, "pageSize": pageSize, "count": int(
            math.ceil(total)), "allPage": int(math.ceil(totalPage)), "results": data_list}

        return jsonify(pageInfo)
    if request.method == 'POST':
        nid = request.args.get('nid')
        print("Request,", nid)
        result = info.query.filter_by(id=nid).first()
        db.session.delete(result)
        db.session.commit()
        rsp = {
            "message": "删除成功"
        }
        return jsonify(rsp)
