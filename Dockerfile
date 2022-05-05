FROM python:3.8-slim
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
EXPOSE 1701
CMD [ "python", "main.py", "1701" ]