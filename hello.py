# -------------------------------
# -*- coding: utf-8 -*- 
# @Time : 2019/5/16 23:33 
# @Author : monarch
# @Site :  
# @File : hello.py.py 
# @Software: PyCharm
# -------------------------------
from datetime import datetime

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
Bootstrap(app)
moment = Moment(app)


@app.route("/")
def index():
    return render_template("index.html", current_time=datetime.utcnow())


if __name__ == "__main__":
    app.run()
