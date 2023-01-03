from concurrent import futures
import logging

import grpc
import dfs_pb2
import dfs_pb2_grpc
import yaml
import os
global_node_id  = int(os.getenv('NODE_ID'))
PORT = int(os.getenv('PORT'))

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
        with open("neighbours.yml", 'r') as f:
            dict_nb = yaml.safe_load(f)
        neighbours_node = dict_nb[int(global_node_id)]
        with open("ip_configuration.yml",'r') as file_ip:
            dict_ip = yaml.safe_load(file_ip)
        for nb in neighbours_node:
            self.neighbors[str(nb)]=str(dict_ip.get(nb))
            self.unexplored.append(str(nb))
        
        print(self.neighbors)
    
    #this function will start this node as the root and communicate to all neighbors
    def MakeRoot(self, request, context):
        if(self.unexplored): #If there are still unexplored nodes at the root
            #when root is called on a node, this means it has no parent, or it is its own parent
            print("Make Root call \n") #for DEBUG / DELETE
            self.parent = self.node
            while self.unexplored: #while there are unexplored neighbors, message them
                neighbor = self.unexplored.pop() #pops neighbor from the list
                ip = self.neighbors[neighbor]+':'+str(PORT)
                with grpc.insecure_channel(ip) as channel:
                    stub = dfs_pb2_grpc.DFSStub(channel) 
                    #send message to neighbor
                    print("Sending message to" + str(neighbor) + " \n") #for DEBUG / DELETE
                    response = stub.SendForward(dfs_pb2.ForwardMessage(type=1, origin=int(self.node)))
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
                ip = self.neighbors[neighbor]+':'+str(PORT)
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
            root_ip = self.neighbors[str(self.parent)]+':'+str(PORT)
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
            root_ip = self.neighbors[str(self.parent)]+':'+str(PORT)
            with grpc.insecure_channel(root_ip) as channel:
                    stub = dfs_pb2_grpc.DFSStub(channel)
                    print("Sending infomation upward to " + str(self.parent) + "\n")
                    response = stub.SendBackward(dfs_pb2.BackwardMessage(type=1, child=request.child, parent=request.parent))
            return dfs_pb2.BackwardReply(type=1)
        return super().SendBack(request, context)
    
        
    def ResetNetworkSvc(self, request, context):
        #send reset message down the network (to the children only)
        for child in self.children:
            ip = self.neighbors[str(child)]+':'+str(PORT)
            with grpc.insecure_channel(ip) as channel:
                stub = dfs_pb2_grpc.DFSStub(channel)
                response = stub.ResetNetworkSvc(dfs_pb2.ResetNetworkRequest(type=1))
        
        #reset the node state 
        self.neighbors = {} #dictionary with node name and IP
        self.parent = -1
        self.children = []
        self.unexplored = []
        self.tree_children = []
        self.tree_parents = []
        
        #read initialization file
        with open("neighbours.yml", 'r') as f:
            dict_nb = yaml.safe_load(f)
        neighbours_node = dict_nb[int(global_node_id)]
        with open("ip_configuration.yml",'r') as file_ip:
            dict_ip = yaml.safe_load(file_ip)
        for nb in neighbours_node:
            self.neighbors[str(nb)]=str(dict_ip.get(nb))
            self.unexplored.append(str(nb))
        
        return dfs_pb2.ResetNetworkReply(type=1)
        

    
def serve():
    port = str(PORT)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dfs_pb2_grpc.add_DFSServicer_to_server(DFS(), server)
    server.add_insecure_port('[::]:' + port)
    
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    print("test")
    logging.basicConfig()
    serve()
