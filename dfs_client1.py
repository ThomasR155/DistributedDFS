from concurrent import futures
import logging

import grpc
import dfs_pb2
import dfs_pb2_grpc

global_node_id = 1

class Greeter(dfs_pb2_grpc.GreeterServicer):

    def __init__(self):
        self.node = global_node_id
        self.neighbors = {} #dictionary with node name and IP
        #read initialization file
        with open("Node"+str(self.node)+".txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.neighbors[str(line.split()[0])] = str(line.split()[1])
        
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
        self.node = global_node_id
        self.neighbors = {} #dictionary with node name and IP
        self.parent = -1
        self.children = []
        self.unexplored = []
        self.tree_children = []
        self.tree_parents = []

        #read initialization file
        with open("Node"+str(self.node)+".txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.neighbors[str(line.split()[0])] = str(line.split()[1])
                self.unexplored.append(str(line.split()[0]))
        
        print(self.neighbors)
    
    #this function will start this node as the root and communicate to all neighbors
    def MakeRoot(self, request, context):
        if(self.unexplored): #If there are still unexplored nodes at the root
            #when root is called on a node, this means it has no parent, or it is its own parent
            print("Make Root call \n") #for DEBUG / DELETE
            self.parent = self.node
            while self.unexplored: #while there are unexplored neighbors, message them
                neighbor = self.unexplored.pop() #pops neighbor from the list
                ip = 'localhost:' + self.neighbors[neighbor]
                with grpc.insecure_channel(ip) as channel:
                    stub = dfs_pb2_grpc.DFSStub(channel) 
                    #send message to neighbor
                    print("Sending message to" + str(neighbor) + " \n") #for DEBUG / DELETE
                    response = stub.SendForward(dfs_pb2.ForwardMessage(type=1, origin=self.node))
                    if response.type == 1: #if neighbor accepts, becomes children
                        self.children.append(neighbor)
                        print(str(neighbor), "accepted parent\n")
                    else: #if refuses, nothing changes
                        print(str(neighbor), "refused parent\n")
                    #add roots children to tree
        for i in range(0, len(self.children)):
            self.tree_children.append(int(self.children[i]))
            self.tree_parents.append(self.node)
        return dfs_pb2.TreeMessage(type=1, child=self.tree_children, parent=self.tree_parents)

    #the function, actually means the server received a message from another node
    def SendForward(self, request, context):
        if self.parent == -1: #if the node has no parent, first contact will become parent
            self.parent = request.origin
            print("Parent: " + str(self.parent))
            self.unexplored.remove(str(self.parent)) #removes parent from unexplored
            while self.unexplored: #while there are unexplored neighbors, message them
                neighbor = self.unexplored.pop() #pops neighbor from the list
                ip = 'localhost:' + self.neighbors[neighbor]
                print("Sending message to" + str(neighbor) + " \n") #for DEBUG / DELETE
                with grpc.insecure_channel(ip) as channel:
                    stub = dfs_pb2_grpc.DFSStub(channel)
                    #send message to neighbor
                    response = stub.SendForward(dfs_pb2.ForwardMessage(type=1, origin=self.node))
                    if response.type == 1: #if neighbor accepts, becomes children
                        self.children.append(neighbor)
                        print(str(neighbor), "accepted parent\n")
                    else: #if refuses, nothing changes
                        print(str(neighbor), "refused parent\n")
            #add node children to tree
            for i in range(0, len(self.children)):
                self.tree_children.append(int(self.children[i]))
                self.tree_parents.append(self.node)
            #after finishing exploring neighbors, send the children-parent back to the root
            root_ip = 'localhost:' + self.neighbors[str(self.parent)]
            with grpc.insecure_channel(root_ip) as channel:
                    stub = dfs_pb2_grpc.DFSStub(channel)
                    for i in range(0, len(self.children)):
                        #send each pair of child and parent
                        print("Sending infomation upward to " + str(self.parent) + "\n")
                        response = stub.SendBackward(dfs_pb2.BackwardMessage(type=1, child=int(self.children[i]), parent=self.node))
            return dfs_pb2.ForwardReply(type=1) 
        elif(self.parent == request.origin): #if node already has a parent and is the contacting neighbor
            return dfs_pb2.ForwardReply(type=3)
        else: #node has another parent
            return dfs_pb2.ForwardReply(type=2)
        return super().SendMSG(request, context)
    
    #backwards messages are sent through the network until reaching the
    def SendBackward(self, request, context):
        print("Received bacward message \n") #for DEBUG / DELETE
        #add information to the tree (might be partial)
        self.tree_children.append(request.child)
        self.tree_parents.append(request.parent)
        
        #check if node is the root
        if (self.parent == self.node):
           #if it is the root, simply return
           print("I am root")
           return dfs_pb2.BackwardReply(type=1)
        else:
            #if it is not the root, then send the message backwards
            root_ip = 'localhost:' + self.neighbors[str(self.parent)]
            with grpc.insecure_channel(root_ip) as channel:
                    stub = dfs_pb2_grpc.DFSStub(channel)
                    print("Sending infomation upward to " + str(self.parent) + "\n")
                    response = stub.SendBackward(dfs_pb2.BackwardMessage(type=1, child=request.child, parent=request.parent))
            return dfs_pb2.BackwardReply(type=1)
        return super().SendBack(request, context)


def serve():
    port = str(50050+global_node_id)
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
