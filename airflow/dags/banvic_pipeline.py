from datetime import datetime, timedelta

from airflow.sdk import dag, task

# Import the FileSensor to wait for files before starting the pipeline
from airflow.providers.standard.sensors.filesystem import FileSensor

# list of CSV datasets that will be processed. Each name corresponds to a source file (<name>.csv)
DATASETS = [
        "agencias",
        "clientes",
        "colaborador_agencia",
        "colaboradores",
        "contas",
        "propostas_credito",
        "transacoes"
    ]

default_args = {
    "retries": 3,                             # Retry failed tasks up to 3 times
    "retry_delay": timedelta(minutes=5),      # Wait 5 minutes between retries
    "retry_exponential_backoff": True,       # Increase wait time exponentially
    "max_retry_delay": timedelta(hours=1),    # Cap exponential delay to 1 hour
}

# Define the Airflow DAG
@dag(
    dag_id='meltano-banvic-pipeline',
    start_date=datetime(2026, 7, 15), # Date from which the scheduler can start creating DAG runs
    default_args=default_args,
    schedule='*/5 * * * * ', # Run every 5 minutes
    catchup=False # Do not run missed schedules from the past
)
def pipeline():

    # Wait for all expected CSV files to be available before ingestion.
    # Dynamic task mapping creates one FileSensor task per dataset.
    wait_for_file = FileSensor.partial(
        task_id='wait_for_file',
        timeout=3600, # 1 hour timeout
        poke_interval=30,  # check every 30 seconds
        fs_conn_id="data_source_path", # Airflow connection pointing to the source data directory, this id was created in airflow UI
        start_from_trigger=False # Execute directly when triggered instead of using the deferrable trigger
    ).expand(
        filepath=[f"/opt/airflow/data/source/{name}.csv" for name in DATASETS] # Generate one sensor for each expected CSV file
    )

    # Bash task that runs a Meltano EL (Extract & Load) job for a single dataset.
    @task.bash()
    def ingestion(name: str):
        return (
            f"cd /opt/airflow/meltano && "
            f"/home/airflow/.local/bin/meltano el "
            f"--state-id=banvic-{name}-pipeline "
            f"tap-csv --select {name} target-postgres"
        )

    wait_for_file >> ingestion.expand(name=DATASETS) # Dynamic task mapping creates one ingestion task per dataset.

pipeline()