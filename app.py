# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:34:26 2022

@author: shangfr
"""

import streamlit as st
from pipdeptree import get_installed_distributions, PackageDAG
from language import chinese_dict
from charts import render_graph

st.set_page_config(page_title='PyDepGraph', page_icon='🌐', layout="wide")
st.sidebar.title('🌐 PyDepGraph')
st.header('PackagesGraph 👇 ')

lang = st.sidebar.select_slider(
    '💬 Select a Language of The App',
    options=['English', '中文'])

if lang == '中文':
    lang_dict = chinese_dict
else:
    lang_dict = {k: k for k, v in chinese_dict.items()}


with st.sidebar:
    st.write(f"#### {lang_dict['Upload your own data']}")
    uploaded_file = st.file_uploader(
        lang_dict["the streamlit data default"], type=['json'])

    col3, col4 = st.columns(2)
    with st.expander(lang_dict['Color Setting']):
        col5, col6, col7, col8 = st.columns(4)

    with st.expander(lang_dict['Nodes Setting']):
        col9, col10 = st.columns(2)
        col11, col12 = st.columns(2)
        col13, col14 = st.columns(2)

    st.markdown('---')


node_color = col5.color_picker(lang_dict['Node Color'], '#00F9F5')
links_color = col6.color_picker(lang_dict['Links Color'], '#F90023')
border_color = col7.color_picker(lang_dict['Border Color'], '#146B6B')
shadow_color = col8.color_picker(lang_dict['Shadow Color'], '#00F9C9')


node_size = col9.slider(lang_dict["Nodes SymbolSize"], 5, 50, 20)
border_width = col10.slider(lang_dict["Border Width"], 0, 10, 2)
shadow_blur = col11.slider(lang_dict["Shadow Blur"], 0, 50, 10)
nodes_font_size = col12.slider(lang_dict["Nodes FontSize"], 5, 50, 12)
label_font_size = col13.slider(lang_dict["Label FontSize"], 5, 50, 10)


@st.cache(allow_output_mutation=True)
def read_pkgs(local_only=True, user_only=False):
    pkgs = get_installed_distributions(local_only, user_only)
    tree = PackageDAG.from_pkgs(pkgs)
    return tree


if uploaded_file is None:
    local_only = True
    user_only = False
    tree = read_pkgs(local_only, user_only)
    packages = col3.text_input(lang_dict['Packages'], value='streamlit')
    exclude = col4.text_input(lang_dict['Exclude'], value='')

    show_only = set(packages.split(",")) if packages else None
    exclude = set(exclude.split(",")) if exclude else None

    if show_only is not None or exclude is not None:
        tree = tree.filter(show_only, exclude)

    data = [{"package": k.as_dict(), "dependencies": [v.as_dict() for v in vs]}
            for k, vs in tree.items()]
else:
    from utils import extract_graph_data
    bytes_data = uploaded_file.getvalue()
    data = extract_graph_data(bytes_data)


item_style = {"normal": {
    "borderColor": border_color,
    "borderWidth": border_width,
    "shadowBlur": shadow_blur,
    "shadowColor": shadow_color,
    "color": node_color
}}

nodes = []
links = []
categories = []


def node_check(node_d, item_style=item_style):
    node_n = node_d['key']
    nn = [n for n in nodes if n.get('name') == node_n]
    if len(nn) == 0:
        node = {}
        node_id = str(len(nodes))
        node['id'] = node_id
        node['name'] = node_d['key']
        node['value'] = node_d['installed_version']
        node['itemStyle'] = item_style
        nodes.append(node)
    else:
        node_id = nn[0]['id']
    return node_id


for d in data:
    node_id_s = node_check(d['package'])
    if d['dependencies']:
        for dd in d['dependencies']:
            node_id_t = node_check(dd, item_style)
            link = {}
            link["source"] = node_id_s
            link["target"] = node_id_t
            link["label"] = {
                "show": True, "formatter": dd['required_version'], "fontSize": label_font_size}
            links.append(link)


graph = {"nodes": nodes, "links": links, "categories": categories}


for idx, _ in enumerate(graph["nodes"]):
    graph["nodes"][idx]["symbolSize"] = node_size

graph["links_color"] = links_color
graph["nodes_font_size"] = nodes_font_size

render_graph(graph)
