FROM python:3.11

RUN apt -y update && \
    apt -y upgrade && \
    apt-get -y --no-install-recommends install \
    chromium

RUN mkdir /usr/src/app 

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
