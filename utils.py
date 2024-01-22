# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 10:22:45 2022

@author: shangfr
"""
import json

def extract_graph_data(bytes_data):
    data = json.loads(bytes_data)
    return data

def process_data_for_visualization(data, item_style, link_style):

    node_tree = data[0]
    nodes = [{"name": node_tree['key'],
              "value":node_tree['installed_version'], "item_style":item_style,'symbolSize':len(node_tree["dependencies"])+1}]
    
    links = []
    nodes_name = []
    
    def rename_key_recursive(node):
        nonlocal nodes, links,nodes_name

        old_key = "dependencies"
        new_key = "children"

        if old_key in node:
            node['value'] = len(node[old_key])
            node[new_key] = node.pop(old_key)
            node['name'] = node.pop('package_name')

            for child_node in node[new_key]:
                child_name = child_node['key']
                child_value = child_node['installed_version']

                if child_name not in nodes_name:
                    nodes.append({'name': child_name, 'value': child_value, 'itemStyle': item_style,'symbolSize':len(child_node["dependencies"])+1})
                    nodes_name.append(child_name)
                
                link = {"source": node['key'], "target": child_name, "label": {
                    "show": link_style["show"], "formatter": child_node['required_version'], "fontSize": link_style["fontSize"]}}
                links.append(link)

                if link_style["remove"]:
                    child_node['children'] = []
                    child_node['name'] = child_node.pop('package_name')
                else:
                    rename_key_recursive(child_node)

        else:
            node[new_key] = node.pop(old_key)
            node['name'] = node.pop('package_name')

    # Start processing with the root node (data[0])
    rename_key_recursive(node_tree)

    return {'data': data, 'nodes': nodes, 'links': links}



def prune_dict_by_level(input_dict, target_level):
    """
    Recursively prune a dictionary up to a certain level.
    
    Parameters:
    - input_dict: The input dictionary to be pruned.
    - target_level: The target level up to which the dictionary should be pruned.
    
    Returns:
    - The pruned dictionary.
    """
    if target_level == 0:
        return {}  # If target level is 0, return an empty dictionary
    
    pruned_dict = {}
    
    for key, value in input_dict.items():
        if isinstance(value, dict):
            # Recursively prune nested dictionaries
            pruned_value = prune_dict_by_level(value, target_level - 1)
            
            if pruned_value:  # Only include non-empty dictionaries
                pruned_dict[key] = pruned_value
        else:
            pruned_dict[key] = value
    
    return pruned_dict

