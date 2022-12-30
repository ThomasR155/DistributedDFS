from __future__ import print_function

import logging

import grpc
import dfs_pb2
import dfs_pb2_grpc
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



def run():
    nodename = '1'
    ip ='localhost:50051'
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    #server 1
    with grpc.insecure_channel(ip) as channel:
        stub = dfs_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(dfs_pb2.HelloRequest(name=nodename))
    print("Greeter client received: " + response.message)

    #call neighbors 
    ip ='localhost:50051'
    with grpc.insecure_channel(ip) as channel:
        stub = dfs_pb2_grpc.GreeterStub(channel)
        response = stub.CallNeighbors(dfs_pb2.CallRequest(name=nodename))
    print("Greeter client received: " + response.message)

    #make root DFS procedure 
    ip ='localhost:50051'
    parents = []
    children = []
    edges = np.empty((0,2), int)
    with grpc.insecure_channel(ip) as channel:
        stub = dfs_pb2_grpc.DFSStub(channel)
        response = stub.MakeRoot(dfs_pb2.RootRequest(type=1))
        for i in range(0, len(response.child)):
            print("Child: " + str(response.child[i]) + "Parent: " + str(response.parent[i]))
            edge = np.sort(np.array([response.parent[i], response.child[i]]))
            edges=np.append(edges,np.array([edge]), axis=0)
            edges = np.unique(edges, axis=0)
                 
   

    G = nx.from_edgelist(edges)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_size=1500, node_color='yellow', font_size=8, font_weight='bold',with_labels=True)
    plt.savefig("mst.png")

 




if __name__ == '__main__':
    logging.basicConfig()
    run()
