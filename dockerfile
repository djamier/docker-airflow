FROM apache/airflow:2.7.1-python3.9

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean

USER airflow
ENV PYTHONPATH=.
COPY --chown=airflow:root ./dags /opt/airflow/dags
COPY --chown=airflow:root ./logs /opt/airflow/logs
COPY --chown=airflow:root ./plugins /opt/airflow/plugins
COPY --chown=airflow:root ./resources /opt/airflow/resources
COPY --chown=airflow:root ./sql /opt/airflow/sql
COPY --chown=airflow:root ./requirements.txt /opt/airflow/requirements.txt

RUN pip install -r /opt/airflow/requirements.txt