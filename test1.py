# !streamlit run test1.py --server.port 6006 --server.enableCORS false


# from streamlit_echarts import st_echarts

# options = {
#     "xAxis": {
#         "type": "category",
#         "data": ["Mon", "Tue", "Yu", "Zhang", "Fri", "Sat", "Sun"],
#     },
#     "yAxis": {"type": "value"},
#     "series": [
#         {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
#     ],
# }


# st_echarts(options=options,theme='dark',renderer='SVG',height=500,width=500)
# from sklearn.manifold import TSNE
import numpy as np
from random import choice
import json,random,os
import streamlit as st
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar,Graph,Scatter
from streamlit_echarts import st_pyecharts
from pyecharts.commons.utils import JsCode
path = os.getcwd()
st.set_page_config(page_title='zyj的测试', page_icon='😎', layout='wide', initial_sidebar_state='auto')



#-----------------全局设置-----------------



#默认宽模式


#隐藏logo
#MainMenu {visibility: hidden;} #隐藏右上角标
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# st.sidebar.selectbox("How would you like to be contacted?",("Email", "Home phone", "Mobile phone"))
st.markdown('<table><tr><td bgcolor=#f8f3f3>这是一个测试：🔊📢</td></tr></table>',unsafe_allow_html=True)
# st.subheader("副标题")

# image =Image.open('捕获1.jpg')
# st.image(image, caption='Sunrise by the mountains',use_column_width=True,width=10)

st.sidebar.header("功能区")

st.sidebar.markdown("---")

act=['知识网络可视化','知识元可视化','知识图谱','测试1']
choice=st.sidebar.selectbox("请选择模块",act)





#-----------------知识网络可视化-----------------

with open(path+"/data/npmdepgraph.min10.json", "r", encoding="utf-8") as f:
    data = json.load(f)
nodes = [
    {
        "x": node["x"],
        "y": node["y"],
        "id": node["id"],
        "name": node["label"],
        "symbolSize": node["size"],
        "itemStyle": {"normal": {"color": node["color"]}},
    }
    for node in data["nodes"]
]

edges = [
    {"source": edge["sourceID"], "target": edge["targetID"]} for edge in data["edges"]
]

def G_visualization(k):
    c = (
        Graph(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add(
            series_name="",
            nodes=nodes[:k],
            links=edges,
            layout="none",
            is_roam=True,
            is_focusnode=True,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=0.5, curve=0.3, opacity=0.7),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
    #     .render("npm_dependencies.html")
    )
    return c


if choice=='知识网络可视化':
    st.sidebar.markdown("---")
    x=st.sidebar.slider('节点数量',100,700)
    st_pyecharts(G_visualization(x),height='600px',width='1000px', key="1")



    
    
#-----------------知识元可视化-----------------
    
w2v2D=pd.read_csv(path+"/data/Google词向量降维.csv")
# data.sort(key=lambda x: x[0])
# x_data = [i[0] for i in scatter_data]
# y_data = [i[1] for i in scatter_data]
def Scatter_visualization(wl):
    scatter_data=w2v2D.iloc[:wl]
    sc=(
        Scatter(init_opts=opts.InitOpts(width="1600px", height="1000px"))
        .add_xaxis(xaxis_data=scatter_data['x'].values.tolist())
        .add_yaxis(
            series_name="",color='#0061b2',symbol='circle',
            y_axis=scatter_data[['y','words']].values.tolist(),
            symbol_size=10,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            datazoom_opts=opts.DataZoomOpts(range_start=-70,range_end=70),
            tooltip_opts=opts.TooltipOpts(is_show=True,trigger="item",formatter=JsCode('''
            function (param) {
                var line1 = 'word:' + param.data[2]+ '<br/>';
                var line2 = 'x: ' + param.data[0] + '<br/>';
                var line3 = 'y: ' + param.data[1] + '<br/>';
                return line1 + line2 + line3 ;
            }
            ''')),
        )
    #     .render("basic_scatter_chart.html")
    )
    return sc

if choice=='知识元可视化' :
    st.sidebar.markdown("---")
    x=st.sidebar.slider('词数量',100,2000)
    st_pyecharts(Scatter_visualization(x),height='550px',width='1000px', key="1")


    
#-----------------知识图谱-----------------    
with open(path+"/data/les-miserables.json", "r", encoding="utf-8") as f:
    j = json.load(f)
nodes2 = j["nodes"]
links2 = j["links"]
categories = j["categories"]
def KG():
    kg = (
        Graph(init_opts=opts.InitOpts(width="1000px", height="600px"))
        .add(
            "",
            nodes=nodes2,
            links=links2,
            categories=categories,
            edge_symbol=['none', 'arrow'],
            layout="none",
            is_rotate_label=True,
            linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
            label_opts=opts.LabelOpts(position="right"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
        )
    #     .render("graph_les_miserables.html")
    )
    return kg

if choice=='知识图谱':
    st.sidebar.markdown("---")
    x=st.sidebar.slider('节点数量',100,700)
    st_pyecharts(KG(),height='550px',width='1000px', key="1")

    
    
#-----------------测试1-----------------   

test1_category=[{'name':'男','color':'green'},{'name':'女','color':'yellow'}]
test1_nodes=[{'name':'张三','symbolSize':120,'category':0},{'name':'李四','symbolSize':80,'category':0},{'name':'小婷','symbolSize':50,'category':1},{'name':'王姐','symbolSize':30,'category':1}]
test1_links=[{'source':'张三','target':'小婷','value': '父亲'},{'source':'张三','target':'李四','value': '兄弟'},{'source':'李四','target':'小婷','value': '父亲'},{'source':'王姐','target':'小婷','value': '母亲'},{'source':'李四','target':'王姐','value': '夫妻'}]

def KG_test1():
    kg_test1 = (
        Graph(init_opts=opts.InitOpts(width="1000px", height="600px"))
        .add(
            "",
            nodes=test1_nodes,
            links=test1_links,
            categories=test1_category,
            edge_symbol=['none', 'arrow'],
            layout="force",
            is_draggable=True,
            repulsion=4000,
            is_rotate_label=True,
            linestyle_opts=opts.LineStyleOpts( curve=0),
            label_opts=opts.LabelOpts(position="right"),
            edge_label=opts.LabelOpts(is_show=True, position="middle", formatter="{c}")
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Graph-Les Miserables"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
        )
#         .render("graph_les_miserables.html")
    )
    return kg_test1


if choice=='测试1':
    st.sidebar.markdown("---")
    x=st.sidebar.slider('节点数量',100,700)
    st_pyecharts(KG_test1(),height='550px',width='1000px', key="1")
