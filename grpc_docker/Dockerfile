FROM ubuntu:latest
RUN apt-get update && apt-get install python-is-python3 python3-pip -y
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
RUN mkdir /grpc-docker
COPY . /grpc-docker
WORKDIR /grpc-docker/ddfs
#ENTRYPOINT ["python -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. --grpc_python_out=. dfs.proto"]