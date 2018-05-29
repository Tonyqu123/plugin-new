FROM node:6.2.0-slim
WORKDIR /root

RUN apt-get update
RUN apt-get install -y git

ADD . /root/
RUN echo `ls /root`

RUN npm install
RUN npm run build