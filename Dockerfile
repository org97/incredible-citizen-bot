FROM python:3.8.2
LABEL maintainer="sumlenny"
RUN apt-get update -y && \
    apt-get install -y python3-pip
COPY . /bot
WORKDIR /bot
RUN pip3 install -r requirements.txt
