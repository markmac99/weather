FROM ubuntu:20.04
RUN apt-get update
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get install -y python3.8 python3-pip git \
   python3.8-tk libxslt-dev python-imaging-tk \
   libopencv-dev python3-opencv \
   ffmpeg imagemagick 

RUN ln -s /usr/bin/python3 /usr/local/bin/python
 
RUN apt-get install -y curl unzip
WORKDIR /root/source
COPY requirements.txt .
RUN pip3 install -v -r requirements.txt
RUN apt-get install -y dnsutils iputils-ping