import base64
import os
from app import create_app, db 
from flask_cors import CORS
from flask import Blueprint, jsonify,send_file,make_response
from flask import *
from processor.AIDetector_pytorch import Detector
import datetime
app = create_app()
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
from pathlib import Path
import cv2,shutil
import core.main
BASE_DIR = os.path.dirname(__file__)

# ALLOWED_EXTENSIONS = set(['png', 'jpg'])
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     file = request.files['file']
#     print(datetime.datetime.now(), file.filename)
#     if file:# and allowed_file(file.filename):
#         src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         print("src_path.",src_path)
#         file.save(src_path)
#         shutil.copy(src_path, './tmp/ct')
#         image_path = os.path.join('./tmp/ct', file.filename)
#         pid, image_info = core.main.c_main(
#             image_path, current_app.model, file.filename.rsplit('.', 1)[1])
#         return jsonify({'status': 1,
#                         'image_url': 'http://127.0.0.1:5003/tmp/ct/' + pid,
#                         'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
#                         'image_info': image_info})

#     return jsonify({'status': 0})


# @app.route("/download", methods=['GET'])
# def download_file():
#     # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
#     return send_from_directory('data', 'testfile.zip', as_attachment=True)


# # show photo
# @app.route('/tmp/<path:file>', methods=['GET'])
# def show_photo(file):
#     if request.method == 'GET':
#         if not file is None:
#             image_data = open(f'tmp/{file}', "rb").read()
#             response = make_response(image_data)
#             response.headers['Content-Type'] = 'image/png'
#             return response

# @app.before_first_request
# def initDB(*args, **kwargs):
#     app.app_context().push() 
#     db.create_all()


if __name__ == "__main__":
    print(app.url_map)
    # with app.app_context():
    #     current_app.model = Detector()
    app.run(host='localhost', port=5013,debug=True, threaded=False)

