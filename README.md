# Starting to work

To start working with docker-airflow you can invoke this command:

```bash
source project.sh
```

This command will do the following things:

- Create `venv` directory if not exist.
- Activate virtual environment.
- Install all pip packages defined in `requirements.txt`


# Start to install airflow

To start pull docker you can invoke this command:

```zsh
docker-compose up -d
```

# Stop working

To stop working with the docker-airflow , you can deactivate the virtual environment:

```zsh
docker-compose down
```

```zsh
deactivate
```