"""
Name: Lam Xin Yi, Jeslyn
Date: 12/10/2021
"""
import ntpath
import os
import random
import re
import time
import tkinter as tk
from tkinter import filedialog as fd

import networkx as nx
from pyvis.network import Network

# create the root window
root = tk.Tk()
root.withdraw()
root.wm_attributes('-topmost', 1)


def print_selection_and_get_response(choices):
    for item in range(len(choices)):
        print(item, ":", choices[item])
    while True:
        try:
            user_input = int(input("USER : "))
            if user_input in list(range(len(choices))):
                return user_input
            else:
                raise ValueError
        except ValueError:
            print("PLEASE TRY AGAIN")
            continue


# ensuring validity of search
def ensured_validity_of_search(graph_nodes, target_nodes):
    # check if all target nodes is in graph nodes
    for item in target_nodes:
        if item not in graph_nodes:
            return False
    return True


def generate_new_file_name(magic_file):
    datetime = time.strftime("%Y%m%d_%H%M%S_")
    script_name = ntpath.basename(magic_file).rsplit('.', 1)[0]
    print("OUTPUT TO", datetime + script_name + ".csv")
    return datetime + script_name + ".csv"


# user selection interface
def select_file(instructions):
    filename = ""
    text_file_extensions = ['*.txt', '*.txT', '*.tXT', '*.Txt', '*.TXt', '*.TXT', '*.tXt']
    filetypes = [
        ('test files', text_file_extensions),
        ('All files', '*'),
    ]
    while filename == "" or filename == ():
        filename = fd.askopenfilename(
            parent=root,
            title=instructions,
            filetypes=filetypes)
    return filename


# user interactive viewing interface
def view_graph(graph_object):
    net = Network(notebook=False, width=1800, height=800)
    net.show_buttons()
    net.hrepulsion()
    net.from_nx(graph_object)
    net.show("output.html")


# ------------------#
# reading of files  #
# ------------------#


# # reading target list (hospital nodes)
def read_target_nodes_file_returns_list(file_path):
    """
    :param file_path: path of file
    :return: contents of file as a list
    """
    # ensure file exists
    if not os.path.isfile(file_path):
        print("Error,", file_path, "does not exist!")
        return None
    with open(file_path, "r") as file:
        file_list = file.readlines()

    # cleaning inputs
    target_list = []
    for line in file_list:
        target_list.append(line.strip())

    # ensuring header is valid
    header = target_list.pop(0)
    match = re.search(r'^#\s([0-9]+?)$', header)
    if not match:
        print("Error, invalid file header!")
        return None
    header_value = int(match.group(1))
    if header_value != len(target_list):
        print("Error, header size does not match number of target nodes in file!")
        return None

    # ensuring target node ids are valid
    for item in target_list:
        match = re.search(r'^[0-9]+?$', item)
        if not match:
            print("Error, invalid target id", item, "found!")
            return None

    print(target_list)

    # return target node ids as a list
    return [int(i) for i in target_list]


# reading graph nodes (road intersections/endpoints)
def read_graph_nodes_file_returns_graph_object(file_path):
    """
    :param file_path: path of file
    :return: contents of file as a list
    """
    # ensuring file exist
    if not os.path.isfile(file_path):
        return None
    with open(file_path, "r") as file:
        for line_number in range(4):
            print(file.readline().strip())
        graph_object = nx.Graph()
        chunk = file.readline()
        while chunk:
            nodes = chunk.strip()
            node_list = nodes.split("\t")
            from_node = int(node_list[0])
            to_node = int(node_list[-1])
            print(from_node, to_node)
            graph_object.add_edge(from_node, to_node)
            chunk = file.readline()
    return graph_object


# -----------------------#
# generating fake data   #
# -----------------------#


def generate_target_nodes_as_list(size, graph_object):
    target_nodes = set()
    while len(target_nodes) < size:
        target_nodes.add(random.choice(list(graph_object.nodes)))
    return list(target_nodes)


def generate_graph_nodes_as_dict(nodes, add_edge_per_node):
    graph = dict()
    for i in range(nodes):
        bound = set(list(range(nodes))) - {i}
        graph[i] = random.sample(list(bound), random.randint(1, add_edge_per_node))
    return graph


def generate_disconnected_graph_nodes_as_graph_object(nodes, add_edge_per_node):
    graph = dict()
    for i in range(nodes):
        bound = set(list(range(nodes))) - {i}
        graph[i] = random.sample(list(bound), random.randint(0, add_edge_per_node))
    return nx.from_dict_of_lists(graph)


def generate_graph_nodes_as_graph_object(nodes, add_edge_per_node):
    graph_dict = generate_graph_nodes_as_dict(nodes, add_edge_per_node)
    return nx.from_dict_of_lists(graph_dict)

# gx = generate_graph_nodes_as_graph_object(100, 3)
# tx = generate_target_nodes_as_list(5, gx)
