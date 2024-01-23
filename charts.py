# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 10:23:44 2022

@author: shangfr
"""
from streamlit_echarts import st_echarts


def render_graph(graph):
    option = {
        "backgroundColor": graph['bg_color'],
        "title": {
            "text": "",
            "subtext": "",
            "top": "top",
            "left": "right",
        },
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {
                    "show": True,
                },
                "restore": {
                    "show": True
                },
                "saveAsImage": {
                    "show": False
                }
            }
        },
        "tooltip": {},
        "legend": [{"data": [a["name"] for a in graph["categories"]]}],
        "series": [
            {
                "name": "Packages",
                "type": "graph",
                "layout": graph["layout"],
                "data": graph["nodes"],
                "links": graph["links"],
                "categories": graph["categories"],
                "lineStyle": {"color": graph["links_color"]},
                "roam": True,
                # "label": {"position": "right"},
                "label": {"show": graph["show_n"], "fontSize": graph["nodes_font_size"]},
                "edgeSymbol": ["none", "arrow"],
                "draggable": True,
                "force": {"repulsion": graph["repulsion_forces"]},
            }
        ],
    }
    st_echarts(option, height="600px")

def render_tree(graph):
    data = graph["data"]
    #rename_key_recursive(data[0])
    
    option = {
        "backgroundColor": graph['bg_color'],
        "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
        "series": [
            {
                "type": "tree",
                "data": data,
                "top": "1%",
                "left": "7%",
                "bottom": "1%",
                "right": "20%",
                "symbolSize": 7,
                "layout": graph["layout"],
                "label": {
                    "position": "left",
                    "verticalAlign": "middle",
                    "align": "right",
                    "fontSize": 9,
                },
                "leaves": {
                    "label": {
                        "position": "right",
                        "verticalAlign": "middle",
                        "align": "left",
                    }
                },
                "emphasis": {"focus": "descendant"},
                "expandAndCollapse": True,
                "animationDuration": 550,
                "animationDurationUpdate": 750,
            }
        ],
    }
    st_echarts(option, height="800px")
