# -------------------------------
# -*- coding: utf-8 -*- 
# @Time : 2019/5/13 16:28 
# @Author : monarch
# @Site :  
# @File : __init__.py.py 
# @Software: PyCharm
# -------------------------------
import json
import os

from example.commons import Collector
from pyecharts import options as opts
from pyecharts.charts import Graph, Page

C = Collector()


@C.funcs
def graph_base() -> Graph:
    nodes = [
        {"name": "结点1", "symbolSize": 10},
        {"name": "结点2", "symbolSize": 20},
        {"name": "结点3", "symbolSize": 30},
        {"name": "结点4", "symbolSize": 40},
        {"name": "结点5", "symbolSize": 50},
        {"name": "结点6", "symbolSize": 40},
        {"name": "结点7", "symbolSize": 30},
        {"name": "结点8", "symbolSize": 20},
    ]
    links = []
    for i in nodes:
        for j in nodes:
            links.append({"source": i.get("name"), "target": j.get("name")})
    c = (
        Graph()
        .add("", nodes, links, repulsion=8000)
        .set_global_opts(title_opts=opts.TitleOpts(title="Graph-基本示例"))
    )
    return c


@C.funcs
def graph_weibo() -> Graph:
    with open("../resources/425.json", "r", encoding="utf-8") as f:
        j = json.load(f)
        nodes, links, categories = j
    c = (
        Graph()
            .add(
            "",
            nodes,
            links,
            categories,
            repulsion=50,
            linestyle_opts=opts.LineStyleOpts(curve=0.2),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="Graph-425关系图"),
        )
    )
    return c


if __name__ == "__main__":
     Page().add(*[fn() for fn, _ in C.charts]).render()
    #graph_base().render()
