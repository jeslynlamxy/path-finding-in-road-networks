"""
Name: Lam Xin Yi, Jeslyn
Date: 12/10/2021

"""

# create the root window
import multi_sourced_multi_path_bfs
import utility

NUMBER_OF_PATHS_TO_FIND = 5
NUMBER_OF_HOSPITALS = 10
NUMBER_OF_NODES = 1000
MAX_HOSPITAL_ID = NUMBER_OF_NODES
MAX_EDGES_PER_NODE = 3

ROAD_NET_FILE_NAME = ["roadNet-TX.txt", "roadNet-PA.txt", "roadNet-CA.txt"]


def select_graph_file():
    file_name = utility.select_file("Select Graph File")
    return utility.read_graph_nodes_file_returns_graph_object(file_name)


def select_target_file():
    file_name = utility.select_file("Select Target File")
    return utility.read_target_nodes_file_returns_list(file_name)


def use_road_net_file():
    road_list = ["Texas road network - Nodes: 1379917 Edges: 3843320",
                 "Pennsylvania road network - Nodes: 1088092 Edges: 3083796",
                 "California road network - Nodes: 1965206 Edges: 5533214"]
    road_response = utility.print_selection_and_get_response(road_list)
    return utility.read_graph_nodes_file_returns_graph_object(ROAD_NET_FILE_NAME[road_response])


def generate_graph_nodes():
    return utility.generate_graph_nodes_as_graph_object(NUMBER_OF_NODES, MAX_EDGES_PER_NODE)


def generate_target_nodes(graph_object):
    return utility.generate_target_nodes_as_list(NUMBER_OF_HOSPITALS, graph_object)


def handle_graphs_by_returning_graph_object(graph_response):
    graph_object = None
    if graph_response == 0:
        graph_object = select_graph_file()
    elif graph_response == 1:
        graph_object = use_road_net_file()
    elif graph_response == 2:
        graph_object = generate_graph_nodes()
    return graph_object


def handle_targets_by_returning_target_list(target_response, graph_object):
    target_list = None
    if target_response == 0:
        target_list = select_target_file()
    elif target_response == 1:
        target_list = generate_target_nodes(graph_object)
    return target_list


def get_number_of_paths(target_list):
    while True:
        try:
            max_number = len(target_list)
            print("VALID NUMBER OF PATHS YOU CAN GENERATE IS 1 TO", max_number)
            user_input = int(input("USER : "))
            if 1 <= user_input <= max_number:
                return user_input
            else:
                raise ValueError
        except ValueError:
            print("PLEASE TRY AGAIN")
            continue


def main():
    # human dictionary
    # target nodes = hospital nodes
    # graph nodes = road intersections and endpoints
    # number of paths required = k = multi path if k can be equal or more than 1

    # value limits
    # h >= 1 and h <= n
    # k >= 1 and k <= h

    print("GENERAL ALGORITHM FOR COMPUTING DISTANCE FROM EACH NODE TO TOP K NEAREST HOSPITAL FOR ANY INPUT OF K")
    print("MULTI PATH MULTI SOURCE BREADTH FIRST SEARCH")

    print("GRAPH SELECTION")
    graph_choices = ["SELECT OWN FILE", "ROAD NET FILES", "RANDOMLY GENERATED GRAPH NODES"]
    graph_response = utility.print_selection_and_get_response(graph_choices)
    graph_object = handle_graphs_by_returning_graph_object(graph_response)
    print("GRAPH SUCCESSFULLY LOADED")

    print("TARGET/HOSPITAL NODES SELECTION")
    target_choices = ["SELECT OWN FILE", "RANDOMLY GENERATED TARGET/HOSPITAL NODES"]
    target_response = utility.print_selection_and_get_response(target_choices)
    target_list = handle_targets_by_returning_target_list(target_response, graph_object)

    print("NUMBER OF PATHS TO SEARCH FOR")
    number_of_paths = get_number_of_paths(target_list)

    if utility.ensured_validity_of_search(graph_object.nodes, target_list):
        if graph_object.number_of_nodes() < 1000:
            utility.view_graph(graph_object)
        print("\nDATA LOADED")
        print("TARGET LIST: ", target_list)
        print("NUMBER OF PATHS: ", number_of_paths)
        tree_dict, current_state_dict = multi_sourced_multi_path_bfs.expand_from_trees(graph_object, target_list,
                                                                                       number_of_paths)
        multi_sourced_multi_path_bfs.get_paths_from_trees(utility.generate_new_file_name(__file__),
                                                          tree_dict,
                                                          current_state_dict,
                                                          number_of_paths)
    else:
        print("INVALID SEARCH INPUT, NOT ALL TARGET NODES IS FOUND IN GRAPH NODES")


if __name__ == "__main__":
    main()
