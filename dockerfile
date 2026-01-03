FROM apache/airflow:slim-latest-python3.12

ENV AIRFLOW_HOME=/opt/airflow

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt



