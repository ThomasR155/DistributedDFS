import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
parents = [1, 2]
children = [2, 0]
edges = []
for i in range(len(parents)):
    edges.append(np.sort([parents[i],children[i]]))
edges_mst = np.unique(edges,axis=0)

vertices = np.unique([parents, children])
vertix_count = vertices.shape[0]
print("edges:",edges_mst)
print("Vertices: ", vertix_count)

        
g = ig.Graph(n=vertix_count, edges= edges_mst)
for i in range(vertix_count):
    g.vs[i]["id"]= i
    g.vs[i]["label"]= str(i)
    
fig, ax = plt.subplots()

ig.plot(g, target=ax)
plt.show()
