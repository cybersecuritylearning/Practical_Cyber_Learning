FROM python:3.9.13-bullseye

WORKDIR /server

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN mkdir /.ssh && ln -s /run/secrets/host_ssh_key /.ssh/linode

RUN apt-get update