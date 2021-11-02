"""
Name: Lam Xin Yi, Jeslyn
Date: 12/10/2021
Topic: Multi Sourced Multi Path BFS
"""

import random

import networkx as nx
import pandas as pd
from treelib import Tree
from treelib.exceptions import DuplicatedNodeIdError

import utility


# creates initial nodes stats table
def create_nodes_stats(graph_object):
    current_state_dict = {}
    for node in graph_object.nodes:
        current_state_dict[node] = set()
    return current_state_dict


# initialise search object
# creates initial dict of trees
def init_search(target_list, graph_object, current_state_dict):
    # creates a dict of tree objects
    tree_dict = {}
    # for every node in target list make a tree
    for target_node in target_list:
        tree = Tree()
        tree.create_node("Target Node " + str(target_node), target_node)  # root node
        tree_dict[target_node] = tree
    # initialise level 1 for state dict, roots one would be target nodes
    for node in target_list:
        for item in nx.neighbors(graph_object, node):
            tree_dict[node].create_node(item, item, parent=node)
            current_state_dict[item].add(node)
    return tree_dict


# function that lets you view search stats via command line
def view_stats(current_state_dict, tree_dict):
    print(current_state_dict)
    for tree in tree_dict:
        print(tree_dict[tree])


# does the actual search
def expand_from_trees(graph_object, target_list, num_of_paths_required):
    print("PERFORM SEARCH LOOK FOR:", target_list, "GET NUMBER OF PATHS:", num_of_paths_required)
    flagged = True
    current_state_dict = create_nodes_stats(graph_object)
    tree_dict = init_search(target_list, graph_object, current_state_dict)
    while True:
        tree_dict, current_state_dict, count = expand_once(tree_dict, current_state_dict, graph_object, num_of_paths_required)
        # view_stats(current_state_dict, tree_dict)
        if search_complete(current_state_dict, num_of_paths_required):
            return tree_dict, current_state_dict
        if count == 0:
            if not search_complete(current_state_dict, num_of_paths_required):
                if flagged:
                    # should only do road adding treatment once
                    print("Warning, not all nodes have be reached, possible unconnected graph!")
                    graph_object = get_floaters(current_state_dict, graph_object)
                    flagged = False
                else:
                    # new leaf was not detected thus
                    # recalibrate the leaves
                    # and perform a new search
                    print("Additional warning!")
                    flagged = True
                    current_state_dict = create_nodes_stats(graph_object)
                    tree_dict = init_search(target_list, graph_object, current_state_dict)
            else:
                return tree_dict, current_state_dict


# performs one expansion
def expand_once(tree_dict, current_state_dict, graph_object, num_of_paths_required):
    count = 0
    for tree in tree_dict:
        for node in tree_dict[tree].leaves():
            try:
                queue = []
                for item in nx.neighbors(graph_object, node.tag):
                    try:
                        tree_dict[tree].create_node(item, item, parent=node.tag)
                        if item in current_state_dict:
                            current_state_dict[item].add(tree_dict[tree].root)
                            count += 1
                            queue.append(item)

                    except DuplicatedNodeIdError:
                        continue
                    finally:
                        continue
            except nx.exception.NetworkXError:
                continue
        # if search_complete(current_state_dict, num_of_paths_required):
        #     return tree_dict, current_state_dict, count
    print("Number of Nodes Pending: ", count)
    return tree_dict, current_state_dict, count


# checks if all nodes are hit
def search_complete(current_state_dict, num_of_paths_required):
    return len(min(current_state_dict.values(), key=len)) >= num_of_paths_required


# get nodes who were forgotten about, and not connected
def get_floaters(current_state_dict, graph_object):
    added_edges = []
    # get all nodes with paths not found yet
    unconnected = []
    all_nodes = list(nx.nodes(graph_object))
    for node in all_nodes:
        if current_state_dict[node] == set():
            unconnected.append(node)
    # get suitable nodes with only one edge
    # (assuming those with only one edge are the ones more 'outside')
    suitable_nodes = []
    graph_dict = nx.to_dict_of_lists(graph_object)
    for key, value in current_state_dict.items():
        number_of_edges = len(graph_dict[key])
        if number_of_edges == 1:
            suitable_nodes.append(key)
    # for all unconnected nodes, add edge with those nodes with only one edge
    for item in unconnected:
        chosen_node = random.choice(suitable_nodes)
        graph_object.add_edge(item, chosen_node)
        added_edges.append((item, chosen_node))
    print("ADDED EDGES: ", added_edges)
    utility.view_graph(graph_object)
    return graph_object


# get all paths output
def get_paths_from_trees(output_file_name, tree_dict, current_state_dict, num_of_paths_required):
    paths_to_target_nodes = []
    header = ["source_node", "path", "distance"]
    print(header)
    for node, hosp in current_state_dict.items():
        paths = []
        for target, tree in tree_dict.items():
            if tree.contains(node):
                paths.append(list(tree.rsearch(node)))
        paths.sort(key=len)

        for times in range(num_of_paths_required):
            try:
                path = paths[times]
                distance = len(path)
                row = [node, path, distance]
                print(row)
                paths_to_target_nodes.append(row)
            except IndexError:
                continue
    stats_df = pd.DataFrame(paths_to_target_nodes, columns=header)
    stats_df.to_csv(output_file_name)


def main():
    # generated graph quick demo
    target_list = [5, 10, 15, 20, 25]
    num_of_paths_required = 3

    # test connected
    # demo 1
    generated_graph_object = utility.generate_graph_nodes_as_graph_object(300, 2)
    utility.view_graph(generated_graph_object)
    tree_dict, current_state_dict = expand_from_trees(generated_graph_object, target_list, num_of_paths_required)
    get_paths_from_trees(utility.generate_new_file_name(__file__),
                         tree_dict,
                         current_state_dict,
                         num_of_paths_required)

    # test unconnected
    # demo 2
    generated_graph_object = utility.generate_disconnected_graph_nodes_as_graph_object(300, 2)
    utility.view_graph(generated_graph_object)
    tree_dict, current_state_dict = expand_from_trees(generated_graph_object, target_list, num_of_paths_required)
    get_paths_from_trees(utility.generate_new_file_name(__file__),
                         tree_dict,
                         current_state_dict,
                         num_of_paths_required)


if __name__ == "__main__":
    main()
