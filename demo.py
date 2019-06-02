# -------------------------------
# -*- coding: utf-8 -*- 
# @Time : 2019/5/13 18:43 
# @Author : monarch
# @Site :  
# @File : demo.py 
# @Software: PyCharm
# -------------------------------
import os
from datetime import datetime
from antlr4 import FileStream, CommonTokenStream
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from pyecharts import options
from pyecharts.charts import Graph
from werkzeug.utils import secure_filename

from python.MyVisitor import MyVisitor
from python.cGrammer.CLexer import CLexer
from python.cGrammer.CParser import CParser

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))


app = Flask(__name__, static_folder="templates")
Bootstrap(app)
moment = Moment(app)


def graph_base(prolog,filename) -> Graph:
    nodes = []
    links = []
    categoriesSet = set()
    categories = []
    for x in prolog.keys():
        p = prolog[x]
        if p.value == '':
            p.value = p.name
        if p.id == 1:
            nodes.append({"name": str(p.id) + '.' + p.value,
                          "category": p.name,
                          "draggable": True,
                          'symbolSize': 50
                          })
        else:
            nodes.append({"name": str(p.id) + '.'+ p.value,
                          "category": p.name,
                          "draggable": True,
                          'symbolSize': 5*p.getChildrenCount()+ 10
                          })
        categoriesSet.add(p.name)
        for c in p.children_id:
                links.append({"source": str(p.id) + '.' + p.value, "target": str(prolog[c].id) + '.' + prolog[c].value})
    for x in categoriesSet:
        categories.append({'name': x})

    c = (
        Graph()
            .add(filename,
                 nodes,
                 links,
                 categories,
                 is_rotate_label=True,#旋转标签
                 layout='force',
                 repulsion=500,
                 linestyle_opts=options.LineStyleOpts(curve=0.2),
                 label_opts=options.LabelOpts(is_show=True)#设置是否直接显示node中的name
                 )
            .set_global_opts()
    )
    c.render()

    return c


def translate_c(file,filename):
    # file = './resources/cFile/hello.c'
    inputs = FileStream(file)
    lexer = CLexer(inputs)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.compilationUnit()
    mv = MyVisitor()
    mv.visit(tree)
    # for x in mv.prolog_list.keys():
    #     prolog = mv.prolog_list[x]
    #     prolog.toString()
    return graph_base(mv.prolog_list,filename)


ALLOWED_EXTENSIONS = {'txt', 'c'}  # 允许上传的文件类型
UPLOAD_FOLDER = r'D:\source\python\translatorSystem\resources\cFile'   # 保存路径
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):   # 验证上传的文件名是否符合要求，文件名必须带点并且符合允许上传的文件类型要求，两者都满足则返回 true
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':   # 如果是 POST 请求方式
        file = request.files['file']   # 获取上传的文件
        if file and allowed_file(file.filename):   # 如果文件存在并且符合要求则为 true
            filename = secure_filename(file.filename)  # 获取上传文件的文件名
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)  # 保存文件
            c = translate_c(path,filename)
            return Markup(c.render_embed())
    elif request.method == 'GET':
        return render_template("index.html", current_time=datetime.utcnow())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
