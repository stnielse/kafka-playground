FROM python:3.11-slim

WORKDIR /app
COPY consumer.py /app

RUN pip install confluent-kafka

CMD ["python", "consumer.py"]
