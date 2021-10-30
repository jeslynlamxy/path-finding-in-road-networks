"""
Name: Lam Xin Yi, Jeslyn
Date: 12/10/2021

"""
import time

import networkx as nx
import pandas as pd

import multi_sourced_single_path_bfs
import single_sourced_single_path_bfs
import utility

DEFAULT_NUMBER_OF_NODES = 1000
DEFAULT_NUMBER_OF_MAX_EDGES = 3


# hospital h
# paths needed k
# nodes n


def get_time():
    return time.perf_counter()


def benchmark_n(file_name):
    timings = []
    for value in range(10, 100000):
        print("AT: ", value)
        graph = utility.generate_graph_nodes_as_graph_object(value, 3)
        graph_dict = nx.to_dict_of_lists(graph)
        target_list = utility.generate_target_nodes_as_list(1, graph)

        ms_sp_start_time = get_time()
        multi_sourced_single_path_bfs.expand_from_multiple_nodes(graph, target_list)
        ms_sp_stop_time = get_time()
        ms_sp_time_taken = calculate_time_taken(ms_sp_start_time, ms_sp_stop_time)

        # ss_sp_start_time = get_time()
        # single_sourced_single_path_bfs.all_nodes_to_get_shortest_path_to_any_target_node(graph_dict, target_list)
        # ss_sp_stop_time = get_time()
        # ss_sp_time_taken = calculate_time_taken(ss_sp_start_time, ss_sp_stop_time)

        timings.append([value, ms_sp_time_taken])

    header = ["number_of_nodes", "multi_source_timing", "single_source_timing"]
    stats_df = pd.DataFrame(timings, columns=header)
    stats_df.to_csv(file_name)


def benchmark_h(file_name):
    number_of_nodes = 5000
    max_edges_per_node = 3
    graph = utility.generate_graph_nodes_as_graph_object(number_of_nodes, max_edges_per_node)
    graph_dict = nx.to_dict_of_lists(graph)
    timings = []

    # NUMBER OF HOSPITALS CHANGE FROM 1 TO 1000
    # PATHS TO SEARCH IS ONE

    for value in range(1, number_of_nodes):
        target_list = utility.generate_target_nodes_as_list(value, number_of_nodes)

        ms_sp_start_time = get_time()
        multi_sourced_single_path_bfs.expand_from_multiple_nodes(graph, target_list)
        ms_sp_stop_time = get_time()
        ms_sp_time_taken = calculate_time_taken(ms_sp_start_time, ms_sp_stop_time)

        ss_sp_start_time = get_time()
        single_sourced_single_path_bfs.all_nodes_to_get_shortest_path_to_any_target_node(graph_dict, target_list)
        ss_sp_stop_time = get_time()
        ss_sp_time_taken = calculate_time_taken(ss_sp_start_time, ss_sp_stop_time)

        timings.append([value, ms_sp_time_taken, ss_sp_time_taken])

    header = ["number_of_hospitals", "multi_source_timing", "single_source_timing"]
    stats_df = pd.DataFrame(timings, columns=header)
    stats_df.to_csv(file_name)


def benchmark_k(file_name):
    number_of_nodes = 5000
    max_edges_per_node = 3
    graph = utility.generate_graph_nodes_as_graph_object(number_of_nodes, max_edges_per_node)
    graph_dict = nx.to_dict_of_lists(graph)
    number_of_hospitals = 100
    target_list = utility.generate_target_nodes_as_list(number_of_hospitals, number_of_nodes)
    timings = []

    # NUMBER OF PATHS TO FIND CHANGE FROM 1 TO 100

    for value in range(1, number_of_hospitals):
        ms_mp_start_time = get_time()
        multi_sourced_single_path_bfs.expand_from_multiple_nodes(graph, target_list)
        ms_mp_stop_time = get_time()
        ms_mp_time_taken = calculate_time_taken(ms_mp_start_time, ms_mp_stop_time)

        ss_mp_start_time = get_time()
        single_sourced_single_path_bfs.all_nodes_to_get_shortest_path_to_any_target_node(graph_dict, target_list)
        ss_mp_stop_time = get_time()
        ss_mp_time_taken = calculate_time_taken(ss_mp_start_time, ss_mp_stop_time)

        timings.append([value, ms_mp_time_taken, ss_mp_time_taken])

    header = ["number_of_paths", "multi_source_timing", "single_source_timing"]
    stats_df = pd.DataFrame(timings, columns=header)
    stats_df.to_csv(file_name)


def calculate_time_taken(start_time, stop_time):
    time_taken = stop_time - start_time
    print(f"COMPLETED IN {time_taken:0.10f} SECONDS")
    return time_taken


def main():
    # benchmark_h("2210_test_benchmark_h.csv")
    # benchmark_n("2210_test_benchmark_n.csv")
    # benchmark_k("2210_test_benchmark_k.csv")

    # benchmark_h("2910_test_benchmark_h.csv")
    benchmark_n("2910_test_benchmark_n.csv")
    # benchmark_k("2910_test_benchmark_k.csv")


if __name__ == "__main__":
    main()
