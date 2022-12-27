from concurrent import futures
import logging

import grpc
import dfs_pb2
import dfs_pb2_grpc


class Greeter(dfs_pb2_grpc.GreeterServicer):

    def __init__(self):
        self.node = 1
        self.neighbors = {} #dictionary with node name and IP
        #read initialization file
        with open("Node"+str(self.node)+".txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.neighbors[line.split()[0]] = line.split()[1]
        
        print(self.neighbors)

    def SayHello(self, request, context):
        return dfs_pb2.HelloReply(message=('Hello, %s! from ' % request.name) + str(self.node))

    def CallNeighbors(self, request, context):
        for n in self.neighbors:
            ip = 'localhost:' + self.neighbors[n]
            response = ""
            with grpc.insecure_channel(ip) as channel:
                stub = dfs_pb2_grpc.GreeterStub(channel)
                response = stub.SayHello(dfs_pb2.HelloRequest(name=str(self.node)))
                #response = "default"
        return dfs_pb2.CallReply(message=response.message)

class DFS(dfs_pb2_grpc.DFSServicer):
    
    #initialize node with information about neighbors
    def __init__(self):
        self.node = 1
        self.neighbors = {} #dictionary with node name and IP
        self.parent = None
        self.children = []
        self.unexplored = []
        self.tree_children = []
        self.tree_parents = []

        #read initialization file
        with open("Node"+str(self.node)+".txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.neighbors[line.split()[0]] = line.split()[1]
                self.unexplored.append(line.split()[0])
        
        print(self.neighbors)
    
    #this function will start this node as the root and communicate to all neighbors
    def MakeRoot(self, request, context):
        #when root is called on a node, this means it has no parent, or it is its own parent
        self.parent = self.node
        while self.unexplored: #while there are unexplored neighbors, message them
            neighbor = self.unexplored.pop() #pops neighbor from the list
            ip = 'localhost:' + self.neighbors[neighbor]
            with grpc.insecure_channel(ip) as channel:
                stub = dfs_pb2_grpc.DFSStub(channel) 
                #send message to neighbor
                response = stub.SendForward(dfs_pb2.ForwardMessage(type=1, origin=self.node))
                if response == 1: #if neighbor accepts, becomes children
                    self.children.append(neighbor)
                else: #if refuses, nothing changes
                    print(str(neighbor), "refused parent\n")


        return dfs_pb2.TreeMessage(type=1, child=self.tree_children, parent=self.tree_parents)

    #the function, actually means the server received a message from another node
    def SendForward(self, request, context):
        if self.parent == None: #if the node has no parent, first contact will become parent
            self.parent = request.origin
            while self.unexplored: #while there are unexplored neighbors, message them
                neighbor = self.unexplored.pop() #pops neighbor from the list
                ip = 'localhost:' + self.neighbors[neighbor]
                with grpc.insecure_channel(ip) as channel:
                    stub = dfs_pb2_grpc.DFSStub(channel)
                    #send message to neighbor
                    response = stub.SendForward(dfs_pb2.ForwardMessage(type=1, origin=self.node))
                    if response == 1: #if neighbor accepts, becomes children
                        self.children.append(neighbor)
                    else: #if refuses, nothing changes
                        print(str(neighbor), "refused parent\n")
            #after finishing exploring neighbors, send the children-parent back to the root
            root_ip = 'localhost:' + self.neighbors[self.parent]
            with grpc.insecure_channel(root_ip) as channel:
                    stub = dfs_pb2_grpc.DFSStub(channel)
                    for i in range(0, len(self.children)):
                        #send each pair of child and parent
                        response = stub.SendBackward(dfs_pb2.BackwardMessage(type=1, child=self.children[i], parent=self.node))
            return dfs_pb2.ForwardReply(type=1) 
        elif(self.parent == request.origin): #if node already has a parent and is the contacting neighbor
            return dfs_pb2.ForwardReply(type=3)
        else: #node has another parent
            return dfs_pb2.ForwardReply(type=2)
        return super().SendMSG(request, context)
    
    #backwards messages are sent through the network until reaching the
    def SendBackward(self, request, context):

        #add information to the tree (might be partial)
        self.tree_children.append(request.child)
        self.tree_parents.append(request.parent)
        
        #check if node is the root
        if (self.parent == self.node):
           #if it is the root, simply return
           return dfs_pb2.BackwardReply(type=1)
        else:
            #if it is not the root, then send the message backwards
            root_ip = 'localhost:' + self.neighbors[self.parent]
            with grpc.insecure_channel(root_ip) as channel:
                    stub = dfs_pb2_grpc.DFSStub(channel)
                    for i in range(0, len(self.children)):
                        #send each pair of child and parent
                        response = stub.SendBackward(dfs_pb2.BackwardMessage(type=1, child=request.child, parent=request.parent))
            return dfs_pb2.BackwardReply(type=1)
        return super().SendBack(request, context)


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dfs_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    dfs_pb2_grpc.add_DFSServicer_to_server(DFS(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()