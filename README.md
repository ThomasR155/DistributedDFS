# Semester project in Distributed Algorithms by Raphael Duarte and Thomas Riedl
## Implementation of Distributed Depth-First-Search with gRPC and Docker
### Overview
The task for our semester project was the implementation of the common Depth-First-Search algorithm on a distributed system.
DFS is a graph traversal algorithm which garantees to visit every node and is therefore often used to create a spanning tree.
For this project the graph for traversal is a network of docker containers which resemble the nodes of the graph and are connected via edges.
The communication between the nodes is done via the Python API of gRPC and is utilizing protocol buffers.
The resulting spanning tree shows which connections inside of the network are necessary and which ones are redundant.
### Execution
#### Windows
For the execution of our algorithm on windows there is a .ipynb-notebook provided.
To run the execution notebook an anaconda and docker installation are required.
If these prerequisites are met the code can be executed by following commands (example was done on Windows 11):

    git clone https://github.com/ThomasR155/DistributedDFS
    cd DistributedDFS
    conda create --name ddfs
    conda activate ddfs
    conda install pip jupyter
    pip install -r requirements_host.txt
    cd ddfs
    jupyter notebook dfs_execution.ipynb

#### Linux
For the execution of our algorithm on linux there is a .ipynb-notebook provided.
To run the execution notebook a docker installation is required.
If these prerequisites are met the code can be executed by following commands (example was done on Ubuntu 22.04):

    git clone https://github.com/ThomasR155/DistributedDFS
    cd DistributedDFS
    sudo apt-get install python3-pip jupyter-notebook docker-compose
    sudo groupadd docker
    sudo usermod -aG docker <username>
    pip install -r requirements_host.txt
    cd ddfs
    jupyter notebook dfs_execution.ipynb



### Report
In addition to the implementation of the algorithm a short report is provided. In the report the algorithm and the deployment of the distributed system are explained in detail. There is also more information on how the work was split in between the team members and the algorithm is demonstrated based on some graph examples.