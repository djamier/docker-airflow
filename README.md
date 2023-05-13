# Starting to work

To start working with docker-airflow you can invoke this command:

```bash
source config.sh
```

This command will do the following things:

- Create `venv` directory if not exist.
- Activate virtual environment.
- Install all pip packages defined in `requirements.txt`


# Start to install airflow

To start docker-airflow you can invoke this command:

```zsh
docker-compose up -d
```

After running the command above, your directory will be created like this:

.
├── dags
├── logs/
│   ├── dag_processor_manager
│   └── scheduler
├── plugins
└── data

# Stop working

To stop working with docker-airflow , you can deactivate the virtual environment:

```zsh
docker-compose down
deactivate
```