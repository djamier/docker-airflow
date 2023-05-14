# Starting to work

To start working with docker-airflow you can invoke this command:

```bash
source config.sh
```

This command will do the following things:

- Create `venv` directory if not exist
- Activate virtual environment
- Update to latest pip


# Docker-Airflow Setup

To start Docker-Airflow, you can run the following commands:


```zsh
docker build -t image_airflow .
```
This command will do the following things:
- Build an airflow image
- Install all pip packages defined in `requirements.txt`

```zsh
docker-compose up -d
```
This command will start Airflow and its dependencies in separate Docker containers, and the -d flag runs the containers in detached mode, allowing you to continue using your terminal. After running the command, the directory structure of your project will be created as shown:

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
