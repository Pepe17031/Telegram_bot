FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install psycopg2-binary
RUN pip install python-binance

ENTRYPOINT ["python", "coin_watcher.py"]