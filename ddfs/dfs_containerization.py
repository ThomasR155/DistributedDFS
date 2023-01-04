import yaml
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def plot_input_graph(edge_list):
    G = nx.from_edgelist(edge_list)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_size=1500, node_color='yellow', font_size=14, font_weight='bold',with_labels=True)
    plt.savefig("../output/input_graph.png")

def get_neigbours_yaml(edge_list):
    neighbours = {}
    # all unique numbers in the edge list are vertices
    vertices = np.unique(edge_list)
    # for all vertices look for the neighbours
    for vertex in vertices:
        neighbours_v = []
        # iterate through all edges to check for neighbours
        for edge in edge_list:
            # if vertix is part of edge, the other part of the edge is a neighbour
            if np.any(edge ==vertex):
                neighbour=int(edge[int(np.where(edge != vertex)[0])])
                if neighbour not in neighbours_v:
                    neighbours_v.append(neighbour)
        # sort the neighbours descending for and ordered spanning tree in the end
        neighbours_v.sort(reverse=True)
        neighbours[int(vertex)] = neighbours_v
    # save neighbours to yml file
    with open('neighbours.yml', 'w') as outfile:
        yaml.dump(neighbours, outfile, default_flow_style=False)
    print("direct neighbours for each node:")
    print(neighbours)
    

def write_docker_compose_yml(edge_list,port):
    # all unique numbers in the edge list are vertices
    vertices = np.unique(edge_list)
    compose_file = {}
    compose_file["version"]="3"
    # all nodes are specified inside of services:
    services = {}
    with open("ip_configuration.yml",'r') as file_ip:
        dict_ip = yaml.safe_load(file_ip)
    # use ip configuration
    for v in vertices:
        node=       {"build":
                        {"context": ".",
                         "args":
                            {"PORT":port, "NODE_ID":int(v)}}, 
                    "networks": 
                        {"frontend": 
                            {"ipv4_address": dict_ip.get(int(v))}},
                    "command":"/bin/sh -c 'python3 dfs_server.py'", 
                    "container_name":"node{}".format(int(v)),
                    "volumes":["./output:/grpc-docker/ddfs/output"],
                    }
        services["n{}".format(int(v))]=node

    # all nodes are done
    compose_file["services"]= services

    # configure subnet network
    compose_file["networks"]= {"frontend":
                                    {"ipam":
                                        {"config":
                                            [{"subnet":dict_ip.get("subnet")}],
                                        }
                                    }
                                }      
    #save the compose file          
    with open('../docker-compose.yml', 'w') as outfile:
        yaml.dump(compose_file, outfile, default_flow_style=False)
    print("Initialization of Node 1:")
    print(compose_file["services"]["n1"])
    return vertices