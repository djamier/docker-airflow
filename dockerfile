FROM apache/airflow:2.6.1-python3.9

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean

USER airflow
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /opt/airflow
COPY . .

ENV AIRFLOW_HOME=/opt/airflow

CMD ["airflow", "webserver", "--port", "8080", "--daemon"]
CMD ["airflow", "scheduler"]
