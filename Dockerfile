FROM python:3.8-slim
RUN apt-get update && apt-get install netcat -y && pip install prometheus_client
WORKDIR /code
COPY main.py /code
EXPOSE 1701
CMD [ "python", "main.py", "1701" ]