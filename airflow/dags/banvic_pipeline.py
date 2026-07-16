import os
from datetime import datetime

from airflow.sdk import dag, task
from airflow.providers.standard.sensors.filesystem import FileSensor

def paths_list():
    return [
        "agencias",
        "clientes",
        "colaborador_agencia",
        "colaboradores",
        "contas",
        "propostas_credito",
        "transacoes"
    ]

@dag(
    dag_id='meltano-banvic-pipeline',
    start_date=datetime(2026, 1, 1),
    schedule='',
    catchup=False
)

def pipeline():

    wait_for_file = FileSensor.partial(
        task_id='wait_for_file',
        fs_conn_id="data_source_path",
        start_from_trigger=False
    ).expand(
        filepath=[f"/opt/airflow/data/source/{name}.csv" for name in paths_list()]
    )

    @task.bash()
    def ingestion(name: str):
        return f"cd /opt/airflow/meltano && /home/airflow/.local/bin/meltano el tap-csv --select {name} target-postgres"

    wait_for_file >> ingestion.expand(name=paths_list())

pipeline()