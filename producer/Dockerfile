FROM python:3.11-slim

WORKDIR /app
COPY producer.py /app

RUN pip install confluent-kafka

CMD ["python", "producer.py"]
