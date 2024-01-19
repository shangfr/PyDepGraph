# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:34:26 2022

@author: shangfr
"""
import streamlit as st
from streamlit.logger import get_logger
from pipdeptree._render import render_json_tree

from language import chinese_dict
from charts import render_graph, render_tree
from utils import extract_graph_data, process_data_for_visualization

LOGGER = get_logger(__name__)

st.set_page_config(page_title='PyDepGraph', page_icon='🌐', layout="wide")
st.sidebar.title('🌐 PyDepGraph')
st.header("Find the dependencies of a Python package")
st.caption("PyDepGraph is a web application designed to display information about Python installed packages and their dependencies. 👇 ")

st.write('''
<style>
button {
    height: auto;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
}

[data-testid="column"] {
    width: calc(20% - 1rem) !important;
    flex: 1 1 calc(20% - 1rem) !important;
    min-width: calc(20% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)


lang = st.sidebar.select_slider(
    '💬 Select a Language of The App',
    options=['English', '中文'],
    help='A useful tool for visualizing Python package dependencies.')


if lang == '中文':
    lang_dict = chinese_dict
else:
    lang_dict = {k: k for k, v in chinese_dict.items()}


col01, col02, col03 = st.columns(3)

with st.sidebar:

    with st.expander(lang_dict['Color Setting']):
        col3, col5, col6, col7, col8 = st.columns(5)

    with st.expander(lang_dict['Nodes Setting']):

        col9, col10 = st.columns(2)
        col11, col12 = st.columns(2)
        col13, col14 = st.columns(2)

    with st.expander(lang_dict['Upload your own Data'], expanded=True):
        uploaded_file = st.file_uploader(
            lang_dict['Proceed as follows'], type=['json'])

        st.markdown('''
                ``` bash
                # shows the local python packages
                pip install pipdeptree
                pipdeptree --json-tree > pkg.json
                
                # shows a particular package
                pipdeptree --json-tree -p xxxpkg > xxxpkg.json
                
                ```
                ''')


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


@st.cache_resource
def read_pkgs():
    from pipdeptree._discovery import get_installed_distributions
    from pipdeptree._models import PackageDAG

    pkgs = get_installed_distributions(local_only=True, user_only=False)
    tree = PackageDAG.from_pkgs(pkgs)

    return tree


if uploaded_file is None:
    tree = read_pkgs()
    pkgs = [{"package": k.as_dict(), "dependencies": [v.as_dict()
                                                      for v in vs]} for k, vs in tree.items()]

else:
    data_json = uploaded_file.getvalue()
    pkgs = extract_graph_data(data_json)


if len(pkgs) == 0:
    st.info(lang_dict['Data is Null'])
    st.stop()

pkgs_name = [p['package']['key'] if p.get(
    'package') else p['key'] for p in pkgs]

if "streamlit" in pkgs_name:
    ids = pkgs_name.index("streamlit")
else:
    ids = None

include = col01.selectbox(lang_dict['Package'], options=pkgs_name, index=ids)
if include is None:
    st.stop()

include = [include]

pkgs_name_dependencies = [[cp['key'] for cp in p['dependencies']]
                          for p in pkgs if p['package']['key'] in include]

exclude = col02.multiselect(
    lang_dict['Dependency Exclusions'], options=pkgs_name_dependencies[0])


if include is not None or exclude is not None:
    try:
        pkgs_tree = tree.filter_nodes(include, exclude)
    except Exception as e:
        st.error(lang_dict['Pkg filter_nodes error']+str(e))
        st.stop()
#data_f = filter_local(data, include)


node_style = {"normal": {
    "borderColor": border_color,
    "borderWidth": border_width,
    "shadowBlur": shadow_blur,
    "shadowColor": shadow_color,
    "color": node_color
}}


layout = col03.selectbox(lang_dict['Layout'], [
                         'force', 'circular', 'tree', 'radial'])

show_n = col01.checkbox(lang_dict["Show Installed Version"], value=True)
show_l = col02.checkbox(lang_dict["Show Required Version"], value=True)
remove = col03.checkbox(lang_dict['Remove Branches Nodes'])

link_style = {"show": show_l, "fontSize": label_font_size, "remove": remove}

data_json = render_json_tree(pkgs_tree)
data = extract_graph_data(data_json)
result = process_data_for_visualization(data, node_style, link_style)
# print(result)

if layout in ['tree', 'radial']:
    graph = {"data": result['data'], "layout": layout}
    render_tree(graph)
else:

    graph = {"nodes": result['nodes'],
             "links": result['links'], "categories": []}

    for idx, _ in enumerate(graph["nodes"]):
        graph["nodes"][idx]["symbolSize"] = node_size

    graph["show_n"] = show_n
    graph["nodes_font_size"] = nodes_font_size
    graph["links_color"] = links_color
    graph['bg_color'] = bg_color
    graph["repulsion_forces"] = repulsion_forces
    graph["layout"] = layout

    render_graph(graph)


# st.json({"Packages":data})

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
