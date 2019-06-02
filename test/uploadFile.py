# -------------------------------
# -*- coding: utf-8 -*- 
# @Time : 2019/5/14 0:41 
# @Author : monarch
# @Site :  
# @File : uploadFile.py 
# @Software: PyCharm
# -------------------------------
import os
from flask import Flask, request
# 获取上传文件的文件名
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = r'D:\source\python\translatorSystem'   # 保存路径
ALLOWED_EXTENSIONS = {'txt', 'c'}  # 允许上传的文件类型

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):   # 验证上传的文件名是否符合要求，文件名必须带点并且符合允许上传的文件类型要求，两者都满足则返回 true
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':   # 如果是 POST 请求方式
        file = request.files['file']   # 获取上传的文件
        print(file)
        if file and allowed_file(file.filename):   # 如果文件存在并且符合要求则为 true
            filename = secure_filename(file.filename)   # 获取上传文件的文件名
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   # 保存文件
            return '{} upload successed!'.format(filename)   # 返回保存成功的信息
    # 使用 GET 方式请求页面时或是上传文件失败时返回上传文件的表单页面
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run()
