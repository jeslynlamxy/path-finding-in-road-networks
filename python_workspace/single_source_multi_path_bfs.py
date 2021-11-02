"""
Name: Lam Xin Yi, Jeslyn
Date: 12/10/2021
Topic: Single Sourced Multi Path BFS
"""

import networkx as nx
import pandas as pd

import utility


# single sourced bfs alternative paths (only for small sized graphs)
def all_nodes_to_get_specified_number_of_shortest_paths_to_target_nodes(graph_dict, target_list, paths_needed):
    results_list = []
    graph_nodes = list(graph_dict.keys())
    valid = utility.ensured_validity_of_search(graph_nodes, target_list)
    if not valid:
        print("Invalid search, not all target nodes in list of graph nodes!")
        return None
    graph_nodes = list(graph_dict.keys())
    for source in graph_nodes:
        results_list.append(
            node_to_get_shortest_paths_to_any_target_node(graph_dict, source, target_list, paths_needed))
    return results_list


# single sourced bfs alternative paths (only for small sized graphs)
def node_to_get_shortest_paths_to_any_target_node(graph_dict, source, target_list, paths_needed):
    results_list = []
    ignore_list = []
    if source in target_list:
        return [source]
    while len(ignore_list) < paths_needed:
        try:
            result = next(
                generator_to_search_for_alternative_paths_to_given_target(graph_dict, source, target_list, ignore_list))
            ignore_list.append(result[-1])
            results_list.append(result)
        except StopIteration:
            return None
    return results_list


# single sourced bfs alternative paths (only for small sized graphs)
def generator_to_search_for_alternative_paths_to_given_target(graph_dict, source, target_list, ignore_list):
    queue = [(source, [source])]
    while queue:
        (vertex, path) = queue.pop(0)
        for item in set(graph_dict[vertex]) - set(path):
            if item in target_list and item not in ignore_list:
                yield path + [item]
            else:
                queue.append((item, path + [item]))


def output_paths_from_list(results_list, file_name):
    header = ["source_node", "paths", "distances"]
    print(header)
    results_list_of_list = []
    for paths in results_list:
        if len(paths) == 1:
            row = [paths[0], paths, 0]
            print(row)
            results_list_of_list.append(row)
        else:
            source = paths[0][0]
            distances = []
            for path in paths:
                distances.append(len(path))
            row = [source, paths, distances]
            print(row)
            results_list_of_list.append(row)
    output_df = pd.DataFrame(results_list_of_list, columns=header)
    output_df.to_csv(file_name)


def main():
    # values
    target_list = [5, 10, 15, 20, 25]
    num_of_paths_required = 3
    generated_graph_object = utility.generate_graph_nodes_as_graph_object(100, 3)
    utility.view_graph(generated_graph_object)
    generated_graph_dict = nx.to_dict_of_lists(generated_graph_object)

    # get multiple paths
    print("MULTI PATH")
    results_list = all_nodes_to_get_specified_number_of_shortest_paths_to_target_nodes(generated_graph_dict,
                                                                                       target_list,
                                                                                       num_of_paths_required)
    output_paths_from_list(results_list, utility.generate_new_file_name(__file__))


if __name__ == "__main__":
    main()
