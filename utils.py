# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 10:22:45 2022

@author: shangfr
"""
import json
import networkx as nx


def extract_graph_data(bytes_data):
    data = json.loads(bytes_data)
    return data


def process_data_for_visualization(data, item_style, link_style):
    import copy

    node_tree = copy.deepcopy(data[0])

    nodes_name = []
    nodes = []
    links = []

    def node_check(node):

        name = node['key']
        value = node['installed_version']
        node['value'] = len(node["dependencies"])

        if name not in nodes_name:
            nodes_name.append(name)
            ids = len(nodes_name)
            node_p = {"id": ids-1, "name": name,
                      "value": value,
                      "item_style": item_style,
                      'symbolSize': node['value']+1}

            nodes.append(node_p)

    def rename_key_recursive(node):
        # nonlocal nodes, links, nodes_name

        node_check(node)

        node["children"] = node.pop("dependencies")
        node['name'] = node.pop('package_name')

        for child_node in node["children"]:

            node_check(child_node)

            link = {"source": nodes_name.index(node['key']), "target": nodes_name.index(child_node['key']), "label": {
                "show": link_style["show"], "formatter": child_node['required_version'], "fontSize": link_style["fontSize"]}}
            links.append(link)

            if link_style["remove"]:
                child_node['children'] = []
                child_node['name'] = child_node.pop('package_name')
            else:
                rename_key_recursive(child_node)

    # Start processing with the root node (data[0])
    rename_key_recursive(node_tree)

    # Community Detection using Girvan-Newman

    G = nx.Graph()
    G.add_nodes_from(list(range(len(nodes))))
    G.add_edges_from([(k["source"], k["target"]) for k in links])

    communities = list(nx.community.girvan_newman(G))

    cm = 3 if len(communities) > 3 else -1

    for j, i in enumerate(communities[cm], start=1):
        for ii in i:
            nodes[ii]['category'] = f"Group-{j}"

    return {'data': [node_tree], 'nodes': nodes, 'links': links, "categories": [{"name": f"Group-{nc+1}"} for nc in range(j)]}


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
