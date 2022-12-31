from __future__ import print_function

import logging

import grpc
import dfs_pb2
import dfs_pb2_grpc
import numpy as np
import networkx as nx
import os
import yaml
import matplotlib.pyplot as plt

global_node_id  = int(os.getenv('NODE_ID'))
PORT = int(os.getenv('PORT'))
print(global_node_id)


def run():
    with open("ip_configuration.yml",'r') as file_ip:
        dict_ip = yaml.safe_load(file_ip)
    #ip =str(dict_ip.get(str(global_node_id)))+':'+str(PORT)
    ip ='localhost:'+str(PORT)

    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    #server 1
    with grpc.insecure_channel(ip) as channel:
        stub = dfs_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(dfs_pb2.HelloRequest(name=str(global_node_id)))
    print("Greeter client received: " + response.message)

    #call neighbors 
    with grpc.insecure_channel(ip) as channel:
        stub = dfs_pb2_grpc.GreeterStub(channel)
        response = stub.CallNeighbors(dfs_pb2.CallRequest(name=str(global_node_id)))
    print("Greeter client received: " + response.message)

    #make root DFS procedure 
    edges = np.empty((0,2), int)
    with grpc.insecure_channel(ip) as channel:
        stub = dfs_pb2_grpc.DFSStub(channel)
        response = stub.MakeRoot(dfs_pb2.RootRequest(type=1))
        for i in range(0, len(response.child)):
            print("Child: " + str(response.child[i]) + " Parent: " + str(response.parent[i]))
            edge = np.sort(np.array([response.parent[i], response.child[i]]))
            edges=np.append(edges,np.array([edge]), axis=0)
            edges = np.unique(edges, axis=0)
                 
    G = nx.from_edgelist(edges)
    pos = nx.spring_layout(G)
    color_map = ['red' if node == global_node_id else 'green' for node in G] 
    nx.draw(G, pos, node_size=1500, node_color=color_map, font_size=10, font_weight='bold',with_labels=True)
    plt.savefig("output/mst.png")
 

if __name__ == '__main__':
    logging.basicConfig()
    run()
