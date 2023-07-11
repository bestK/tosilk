ARG PORT=443

FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && \
    apt-get install python3-pip build-essential cmake ffmpeg -y && \
    rm -rf /var/lib/apt/lists/* 

COPY . .

RUN cd /app/lib/silk && make && \
    make encoder && mv encoder /app &&\
    pip install -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT