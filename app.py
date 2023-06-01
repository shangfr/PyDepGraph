# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:34:26 2022

@author: shangfr
"""

import streamlit as st
from streamlit.logger import get_logger
from pipdeptree import get_installed_distributions, PackageDAG
from language import chinese_dict
from charts import render_graph
from utils import extract_graph_data, remove_branches

LOGGER = get_logger(__name__)

st.set_page_config(page_title='PyDepGraph', page_icon='🌐', layout="wide")
st.sidebar.title('🌐 PyDepGraph')
st.header('PackagesGraph 👇 ')

lang = st.sidebar.select_slider(
    '💬 Select a Language of The App',
    options=['English', '中文'],
    help='改变语言将触发app初始化')


if lang == '中文':
    lang_dict = chinese_dict
else:
    lang_dict = {k: k for k, v in chinese_dict.items()}


with st.sidebar:

    col1, col2 = st.columns([1, 2])
    col15, col16 = st.columns([1, 2])
    remove = st.checkbox('Remove Branches Nodes')

    with st.expander(lang_dict['Color Setting']):
        col3, col5, col6, col7, col8 = st.columns(5)

    with st.expander(lang_dict['Nodes Setting']):

        col9, col10 = st.columns(2)
        col11, col12 = st.columns(2)
        col13, col14 = st.columns(2)

    with st.expander(lang_dict['Upload your own Data']):
        uploaded_file = st.file_uploader(
            lang_dict['Proceed as follows'], type=['json'])

        st.markdown('''
                ``` bash
                # shows the local python packages
                pip install pipdeptree
                pipdeptree --json > pkg.json
                
                # shows a particular package
                pipdeptree --json -p xxxpkg > xxxpkg.json
                
                ```
                ''')


layout = col15.selectbox('Layout', ['force', 'circular'])
show_opt = col16.multiselect(
    'Show Pkg',
    [lang_dict["Installed Ver"], lang_dict["Required Ver"]],
    [lang_dict["Required Ver"]])

show_n = lang_dict["Installed Ver"] in show_opt
show_l = lang_dict["Required Ver"] in show_opt


bg_color = col3.color_picker(lang_dict['BG'], '#E9F7F0')
node_color = col5.color_picker(lang_dict['Node'], '#00F9F5')
links_color = col6.color_picker(lang_dict['Links'], '#F90023')
border_color = col7.color_picker(lang_dict['Border'], '#146B6B')
shadow_color = col8.color_picker(lang_dict['Shadow'], '#00F9C9')


node_size = col9.slider(lang_dict["Nodes SymbolSize"], 5, 50, 20)
border_width = col10.slider(lang_dict["Border Width"], 0, 10, 2)
shadow_blur = col11.slider(lang_dict["Shadow Blur"], 0, 50, 10)
nodes_font_size = col12.slider(lang_dict["Nodes FontSize"], 5, 50, 12)
label_font_size = col13.slider(lang_dict["Label FontSize"], 5, 50, 10)
repulsion_forces = col14.slider(lang_dict["Repulsion Forces"], 5, 200, 100)


@st.cache_resource()
def read_pkgs(local_only=True, user_only=False):
    pkgs = get_installed_distributions(local_only, user_only)
    tree = PackageDAG.from_pkgs(pkgs)
    return tree


if uploaded_file is None:
    local_only = True
    user_only = False
    tree = read_pkgs(local_only, user_only)
    packages = col1.text_input(
        lang_dict['Packages'], value='streamlit', help=lang_dict['Comma Separated'])
    exclude = col2.text_input(
        lang_dict['Exclude'], value='pandas,numpy', help=lang_dict['Comma Separated'])

    show_only = set(packages.split(",")) if packages else None
    exclude = set(exclude.split(",")) if exclude else None

    if show_only is not None or exclude is not None:
        try:
            tree = tree.filter(show_only, exclude)
        except Exception as e:
            st.error(lang_dict['Pkg Relationship conflict']+str(e))
            st.stop()

    data = [{"package": k.as_dict(), "dependencies": [v.as_dict() for v in vs]}
            for k, vs in tree.items()]

else:
    bytes_data = uploaded_file.getvalue()
    data = extract_graph_data(bytes_data)

if remove:
    data = remove_branches(data, show_only)

if len(data) == 0:
    st.info(lang_dict['Data is Null'])
    st.stop()

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
                "show": show_l, "formatter": dd['required_version'], "fontSize": label_font_size}
            links.append(link)


graph = {"nodes": nodes, "links": links, "categories": categories}


for idx, _ in enumerate(graph["nodes"]):
    graph["nodes"][idx]["symbolSize"] = node_size

graph["show_n"] = show_n
graph["nodes_font_size"] = nodes_font_size
graph["links_color"] = links_color
graph['bg_color'] = bg_color
graph["repulsion_forces"] = repulsion_forces
graph["layout"] = layout

render_graph(graph)

st.success(
    "**👈 Change graph settings from the sidebar** to design with your own ideas!")

st.markdown(
    """
    PyDepGraph is a utility for displaying the installed python packages in form of a dependency tree.   
    
    ### Want to learn more?
    - Check out 🔎[Streamlit.io](https://streamlit.io)  🔎[Pipdeptree](https://github.com/tox-dev/pipdeptree)  🔎[Echarts](https://echarts.apache.org/)
    - Jump into my [github](https://gitee.com/vencen/py-dep-graph)
    - Contact me <shangfr@foxmail.com>
"""
)
