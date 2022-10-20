# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 10:22:45 2022

@author: shangfr
"""

import json

def extract_graph_data(bytes_data):
    data = json.loads(bytes_data)
    return data