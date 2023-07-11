ARG PORT=443

FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && \
    apt-get install python3-pip build-essential cmake ffmpeg -y && \
    rm -rf /var/lib/apt/lists/* && \
    cd /app/lib/silk && make && make encoder && mv encoder /app

COPY . .

RUN pip install -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT