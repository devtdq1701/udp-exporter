FROM ubuntu:latest
RUN apt-get update && apt-get install netcat python3-pip -y && pip3 install prometheus_client
WORKDIR /code
COPY main.py /code
EXPOSE 1701
CMD [ "python3", "main.py", "1701" ]