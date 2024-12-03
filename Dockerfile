FROM apache/airflow:2.6.3

USER root
RUN apt-get update && apt-get install -y \
    libpq-dev python3-dev

USER airflow
COPY requirements.txt .
RUN pip install -r requirements.txt
