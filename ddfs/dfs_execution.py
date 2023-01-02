# %% [markdown]
# # Semester Project in Distributed Algorithms by Raphael Duarte and Thomas Riedl
# 
# ## Implementation of Distributed Depth-First-Search with gRPC and Docker

# %%
import yaml
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
#own module
import dfs_containerization as dfs_con
import subprocess


# specify the graph of distributed nodes with edge list, all used nodes will be part of the graph
edge_list = [[1,7], [1,2], [1,4], [1,6],
             [2,1], [2,4], [2,3],
             [3,2], [3,4], [3,6], [3,5], [3,7], [3,8], [3,10],
             [4,1], [4,2], [4,3],[4,6], 
             [5,1], [5,3], [5,7],
             [6,4], [6,3], [6,10],
             [7,5], [7,3], [7,8],
             [8,3], [8,7],
             [10,3],[10,6]]

# %%
#plot the input graph
dfs_con.plot_input_graph(edge_list)

# %%
# create an overview of neigbours for each node of the graph and save result as "neighbours.yml"
dfs_con.get_neigbours_yaml(edge_list)

# %%
# specify which IP addresses should be used for the different containers in "ip_configuration.yml"
with open("ip_configuration.yml",'r') as file_ip:
    dict_ip = yaml.safe_load(file_ip)
    print("provided IP configuration for a graph of up to 10 nodes:")
    print(dict_ip)

# %%
#Setup which port should be used for the gRPC communication between the nodes
PORT = 50051

# setup each node as docker container by generating a docker-compose file
dfs_con.write_docker_compose_yml(edge_list, PORT)

# %%
# build docker images of each Node according to generated docker-compose.yml file
process = subprocess.Popen(['docker-compose', 'build'], stdout=subprocess.PIPE, shell=True)
stdout = process.communicate()[0]
print(stdout.decode('utf-8'))


# %%
# start all created docker images as docker containers
# the protocol buffers are being built with start up
# the required code for DDFS is launched with start up (dfs_server.py)
process = subprocess.Popen(['docker-compose', 'up', '-d'], stdout=subprocess.PIPE, shell=True)
stdout = process.communicate()[0]
print(stdout.decode('utf-8'))


# %%
# start the DDFS on the root node
ROOT = 1
# enter the desired docker container and run dfs_client.py which will start the DDFS with the current node as root
process = subprocess.Popen(['docker', 'exec', 'node{}'.format(ROOT), 'python3', 'dfs_client.py'], stdout=subprocess.PIPE, shell=True)
stdout = process.communicate()[0]
print(stdout.decode('utf-8'))

# %%
#plot the minimum spanning tree (saved in output/mst.png)
plt.imshow(plt.imread("../output/mst.png"))
plt.show()


