"""
Name: Lam Xin Yi, Jeslyn
Date: 12/10/2021
Topic: Multi Sourced Single Path BFS
"""
import networkx as nx
import pandas as pd
from treelib import Tree

import utility


def initial_tree(target_list):
    tree = Tree()
    tree.create_node("Ultimate Path Tree", "Target Node")  # root node
    state_dict = {}
    for item in target_list:
        tree.create_node(int(item), int(item), parent="Target Node")
        state_dict[item] = -1
    return state_dict, tree


def expand_from_multiple_nodes(graph_object, target_list):
    # initialise search tree and initial state
    state_dict, tree = initial_tree(target_list)
    total_number_of_nodes = nx.number_of_nodes(graph_object)
    while len(list(state_dict.keys())) != total_number_of_nodes:
        state_dict, target_list = expand_breadth_once(graph_object, target_list, state_dict, tree)
        if not target_list:
            print("Warning, not all nodes have be reached, possible unconnected graph!")
            break
    return tree.paths_to_leaves()


def expand_breadth_once(graph_object, target_list, state_dict, tree):
    new_targets = []
    for target in target_list:
        all_neighbours = nx.neighbors(graph_object, target)
        for item in all_neighbours:
            if item not in state_dict:
                state_dict[item] = True
                tree.create_node(item, item, parent=target)
                new_targets.append(item)
    return state_dict, new_targets


def get_path_from_tree(final_result, file_name):
    header = ["source_node", "path", "distance"]
    # print(header)
    results_list_of_list = []
    for path in final_result:
        path = path[1:]
        path = path[::-1]
        source_node = path[0]
        distance = len(path)
        row = [source_node, path, distance]
        # print(row)
        results_list_of_list.append(row)
    output_df = pd.DataFrame(results_list_of_list, columns=header)
    output_df[["source_node"]] = output_df[["source_node"]].apply(pd.to_numeric)
    output_df = output_df[["source_node", "path", "distance"]].sort_values(by=['source_node'])
    output_df.to_csv(file_name)


def main():
    # generated graph quick demo
    target_list = [5, 10, 15, 20, 25]
    generated_graph_object = utility.generate_graph_nodes_as_graph_object(100, 3)
    utility.view_graph(generated_graph_object)
    tree_dict = expand_from_multiple_nodes(generated_graph_object, target_list)
    get_path_from_tree(tree_dict, utility.generate_new_file_name(__file__))


if __name__ == "__main__":
    main()
