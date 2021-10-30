"""
Name: Lam Xin Yi, Jeslyn
Date: 12/10/2021
"""

import utility


# -----------------------#
# creating of fake files #
# -----------------------#


# creating files containing special target nodes
def create_target_nodes_file(name, size, max_hospital_id):
    target_list = utility.generate_target_nodes_as_list(size, max_hospital_id)
    with open(name, "w") as file:
        header = "# " + str(size)
        file.write(header + "\n")
        for item in target_list:
            file.write(str(item) + "\n")


# creating files containing graph nodes
def create_graph_nodes_file(name, nodes, max_edge_per_node):
    four_lines = ["Hello, this is a artificially generated graph",
                  "Well, why are you looking at this",
                  "Hope you are having a great day",
                  "Bye bye now i am leaving"]
    with open(name, "w") as file:
        for item in four_lines:
            header = "# " + item
            file.write(header + "\n")
    graph_object = utility.generate_graph_nodes_as_graph_object(nodes, max_edge_per_node)
    graph_edges = graph_object.edges
    with open(name, "a") as file:
        for item in graph_edges:
            file.write(str(item[0]) + "\t" + str(item[-1]) + "\n")


def main():
    graph_filename = "roadNet-SG.txt"
    number_of_nodes = 1000
    max_num_of_edges_per_node = 3

    target_filename = "singapore_hospitals.txt"
    number_of_target_nodes = 10
    max_hospital_node_id = 500

    choice = utility.print_selection_and_get_response(
        ["Get Road Network File", "Get Hospital Target Nodes File", "Get Both", "Quit"])
    if choice == 0 or choice == 2:
        create_graph_nodes_file(graph_filename, number_of_nodes, max_num_of_edges_per_node)
    elif choice == 1 or choice == 2:
        create_target_nodes_file(target_filename, number_of_target_nodes, max_hospital_node_id)
    else:
        print(":)")


if __name__ == "__main__":
    main()
