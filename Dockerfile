FROM python:3.5-slim
MAINTAINER Krishna Kumar <kkumar@exathink.com>

RUN apt-get update \
    && apt-get install -y gcc ssh \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r user_grp \
    && useradd -r -g user_grp ec2x \
    && mkdir /home/ec2x \
    && chown ec2x /home/ec2x

COPY . /tmp/build


WORKDIR /tmp/build

RUN pip install --upgrade pip \
    && pip install -r requirements.txt . \
    && apt-get autoremove -y gcc \
    && rm -rf /tmp/build

WORKDIR /home/ec2x

USER EC2X

