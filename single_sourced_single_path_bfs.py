"""
Name: Lam Xin Yi, Jeslyn
Date: 12/10/2021
"""

import networkx as nx
import pandas as pd

import utility


# single sourced bfs (only for small sized graphs)
def all_nodes_to_get_shortest_path_to_any_target_node(graph_dict, target_list):
    results_list = []
    graph_nodes = list(graph_dict.keys())
    valid = utility.ensured_validity_of_search(graph_nodes, target_list)
    if not valid:
        print("Invalid search, not all target nodes in list of graph nodes!")
        return None
    graph_nodes = list(graph_dict.keys())
    for source in graph_nodes:
        results_list.append(node_to_get_shortest_path_to_any_target_node(graph_dict, source, target_list))
    return results_list


# single sourced bfs (only for small sized graphs)
def node_to_get_shortest_path_to_any_target_node(graph_dict, source,
                                                 target_list):  # get the shortest path to any target node
    if source in target_list:
        return [source]
    try:
        return next(generator_to_search_for_path_to_given_target(graph_dict, source, target_list))
    except StopIteration:
        return None


# single sourced bfs (only for small sized graphs)
def generator_to_search_for_path_to_given_target(graph_dict, source, target):
    queue = [(source, [source])]
    while queue:
        (vertex, path) = queue.pop(0)

        for item in set(graph_dict[vertex]) - set(path):
            if item in target:
                yield path + [item]
            else:
                queue.append((item, path + [item]))


def output_paths_from_list(results_list, file_name):
    header = ["source_node", "path", "distance"]
    print(header)
    results_list_of_list = []
    for path in results_list:
        source = path[0]
        distance = len(path)
        row = [source, path, distance]
        print(row)
        results_list_of_list.append(row)
    output_df = pd.DataFrame(results_list_of_list, columns=header)
    output_df.to_csv(file_name)


def main():
    # values
    target_list = [5, 10, 15, 20, 25]
    generated_graph_object = utility.generate_graph_nodes_as_graph_object(100, 3)
    utility.view_graph(generated_graph_object)
    generated_graph_dict = nx.to_dict_of_lists(generated_graph_object)

    # get single paths
    print("SINGLE PATH")
    results_list = all_nodes_to_get_shortest_path_to_any_target_node(generated_graph_dict, target_list)
    output_paths_from_list(results_list, utility.generate_new_file_name(__file__))


if __name__ == "__main__":
    main()
