# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 10:22:45 2022

@author: shangfr
"""

import json
import streamlit as st
import inspect
import textwrap


def extract_graph_data(bytes_data):
    data = json.loads(bytes_data)
    return data

def remove_branches(data, pkg):
    if pkg is None:
        return data
    return [n for n in data if n['package'].get('key') in pkg]

def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", False)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))
