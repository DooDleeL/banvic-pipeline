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

