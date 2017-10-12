FROM ubuntu:16.04

RUN apt-get -y update
RUN apt-get install -y python-dev python-pip
RUN apt-get install -y python-setuptools
#RUN apt-get install -y libmysqlclient-dev

WORKDIR /dailyblog

ADD . /dailyblog


#install any needed pacakges in requirements.txt
RUN pip install -r requirements.txt


#对外暴露端口
EXPOSE 80 8080 8000 5000



#设置环境变量
ENV SPIDER=/tmp















