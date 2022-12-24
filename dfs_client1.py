from __future__ import print_function

import logging

import grpc
import dfs_pb2
import dfs_pb2_grpc



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

    #server 6
    ip ='localhost:50056'
    with grpc.insecure_channel(ip) as channel:
        stub = dfs_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(dfs_pb2.HelloRequest(name=nodename))
    print("Greeter client received: " + response.message)

    #server 7
    ip ='localhost:50057'
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
    with grpc.insecure_channel(ip) as channel:
        stub = dfs_pb2_grpc.DFSStub(channel)
        response = stub.MakeRoot(dfs_pb2.RootRequest(type=1))
        for i in range(0, len(response.child)):
            print("Child: " + str(response.child[i]) + "Parent: " + str(response.parent[i]))


if __name__ == '__main__':
    logging.basicConfig()
    run()