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
            "top": "bottom",
            "left": "right",
        },
        "tooltip": {},
        "legend": [{"data": [a["name"] for a in graph["categories"]]}],
        "series": [
            {
                "name": "Packages",
                "type": "graph",
                "layout": "force",
                "data": graph["nodes"],
                "links": graph["links"],
                "categories": graph["categories"],
                "lineStyle": {"color": graph["links_color"]},
                "roam": True,
                #"label": {"position": "right"},
                "label": {"show": graph["show_n"],"fontSize": graph["nodes_font_size"]},
                "edgeSymbol": ["none", "arrow"],
                "draggable": True,
                "force": {"repulsion": graph["repulsion_forces"]},
            }
        ],
    }
    st_echarts(option, height="500px")
    
    
    
    
    
    