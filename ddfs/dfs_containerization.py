import yaml
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def plot_input_graph(edge_list):
    edges = np.unique(edge_list, axis=1)
    G = nx.from_edgelist(edges)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_size=1500, node_color='yellow', font_size=8, font_weight='bold',with_labels=True)
    plt.savefig("../output/input_graph.png")

def get_neigbours_yaml(edge_list):
    neighbours = {}
    vertices = np.unique(edge_list)
    for vertix in vertices:
        neighbours_v = []
        for edge in edge_list:
            if np.any(edge ==vertix):
                neighbour=int(edge[int(np.where(edge != vertix)[0])])
                if neighbour not in neighbours_v:
                    neighbours_v.append(neighbour)
        neighbours_v.sort(reverse=True)
        neighbours[int(vertix)] = neighbours_v
    with open('neighbours.yml', 'w') as outfile:
        yaml.dump(neighbours, outfile, default_flow_style=False)
    print("direct neighbours for each node:")
    print(neighbours)
    

def write_docker_compose_yml(edge_list,port):
    vertices = np.unique(edge_list)
    compose_file = {}
    compose_file["version"]="3"
    services = {}
    with open("ip_configuration.yml",'r') as file_ip:
        dict_ip = yaml.safe_load(file_ip)
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

    compose_file["services"]= services
    compose_file["networks"]= {"frontend":
                                    {"ipam":
                                        {"config":
                                            [{"subnet":dict_ip.get("subnet")}],
                                        }
                                    }
                                }                
    with open('../docker-compose.yml', 'w') as outfile:
        yaml.dump(compose_file, outfile, default_flow_style=False)
    print("Initialization of Node 1:")
    print(compose_file["services"]["n1"])