FROM apache/airflow:3.3.0-python3.13

USER root
ENV PATH="/home/airflow/.local/bin:${PATH}"
ENV UV_CACHE_DIR=/home/airflow/.uv-cache

RUN mkdir -p ${UV_CACHE_DIR} \
    && chown -R 50000:0 ${UV_CACHE_DIR}

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./airflow/requirements.txt .
COPY ./airflow/scripts /opt/airflow/scripts
COPY ./meltano-banvic/ /opt/airflow/meltano
RUN sed -i 's/\r$//' /opt/airflow/scripts/create_banvic_db.sh && chmod +x /opt/airflow/scripts/create_banvic_db.sh && chmod +x /opt/airflow/meltano

USER airflow
RUN pip install uv==0.11.29 && uv pip install --upgrade pip
RUN uv pip install --no-cache-dir -r requirements.txt