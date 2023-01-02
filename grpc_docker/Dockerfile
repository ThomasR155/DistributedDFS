FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-pip
COPY ./requirements_docker.txt /requirements_docker.txt
RUN pip3 install -r /requirements_docker.txt
RUN mkdir /grpc-docker
COPY . /grpc-docker
WORKDIR /grpc-docker/ddfs
ARG PORT 
ENV PORT "${PORT}"
ARG NODE_ID 
ENV NODE_ID "${NODE_ID}"
RUN ["python3", "-m",  "grpc_tools.protoc" ,"-I." ,"--python_out=.",  "--pyi_out=.", "--grpc_python_out=.", "dfs.proto"]