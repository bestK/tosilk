ARG PORT=443

FROM ubuntu:latest

WORKDIR /app

RUN apt-get update
RUN apt-get install python3-pip build-essential cmake ffmpeg -y
RUN rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT