preriquirements for this project:
docker installed
python 3.13 recommended

the project is already all pre-configured with meltano installing inside the docker container, to edit the configurations for meltano target or tap using the CLI, you can do:
I would suggest creating a virtual venv with:
`py -3.13 -m venv .venv`
activate it 
`source .venv/Scripts/activate`
i also suggest intall the packages with `uv`, to do so:
`pip install uv`
then
`uv pip install -r airflow/requirements.txt`
with this you will have meltano installed in you venv and will be able to use meltano CLI inside `meltano-banvic` folder.

to run:
go to .env.example, fullfill the field with your current values, then rename the file to `.env` only

after that
run the following commands:
`docker compose build`
`docker compose up airflow-init`
`docker compose up -d`

depois de executado, o airflow ficará acessível via: http://localhost:8080
depois de inserido o usuário e senha, go to http://localhost:8080/connections
set a new connection on 'Add Connection'
put the same name as is in the code in airflo/dags/banvic_pipeline 'data_source_path', or choose another one and later alter the `fs_conn_id` parameter

after all that is finished

go to the main page of airflow, select the dag 'meltano-banvic-pipeline'
in the dags page, click 'trigger' and 'trigger' again.

the dag will execute, you can select the tasks and see the logs or the code used.