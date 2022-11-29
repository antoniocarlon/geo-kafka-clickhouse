FROM ubuntu:focal

COPY ./requirements.txt requirements.txt

RUN apt-get update
RUN apt-get install -y python3 python3.8-venv python3-pip

RUN apt-get update
RUN pip3 install --upgrade -r requirements.txt
