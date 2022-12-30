from __future__ import print_function

import logging

import grpc
import dfs_pb2
import dfs_pb2_grpc
import numpy as np
import igraph as ig
import os
import yaml
global_node_id  = os.getenv('NODE_ID')
PORT = os.getenv('PORT')
print(global_node_id)


def run():
    with open("ip_configuration.yml",'r') as file_ip:
        dict_ip = yaml.safe_load(file_ip)
    ip =str(dict_ip.get(str(global_node_id)))+':'+str(PORT)
    ip ='localhost:50051'

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
    parents = []
    children = []
    with grpc.insecure_channel(ip) as channel:
        stub = dfs_pb2_grpc.DFSStub(channel)
        response = stub.MakeRoot(dfs_pb2.RootRequest(type=1))
        print(response.child)
        print(response.parent)
        for i in range(0, len(response.child)):
            print("Child: " + str(response.child[i]) + "Parent: " + str(response.parent[i]))
            parents.append(response.parent[i])
            children.append(response.child[i])
    edges = []
    for i in range(len(parents)):
        edges.append(np.sort([parents[i],children[i]]))
    edges_mst = np.unique(edges,axis=0)

    vertices = np.unique([parents, children])
    vertix_count = vertices.shape[0]
    print("edges:",edges_mst)
    print("Vertices: ", vertix_count)

    edges_mst = edges_mst -1
    g = ig.Graph(n=vertix_count, edges= edges_mst)
    for i in range(vertix_count):
        g.vs[i]["id"]= i+1
        g.vs[i]["label"]= str(i+1)
    
    ig.plot(g, "output/MST.png")
 

if __name__ == '__main__':
    logging.basicConfig()
    run()
