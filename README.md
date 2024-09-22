# ELT-with-dbt

## How to run

1. Clone the repository
2. Install `docker` & `docker-compose`
3. Install dependencies `pip install -r requirements.txt`
4. Run `docker compose up -d`
5. Change working directory to `api_to_postgres`
6. Adjust `checkpointing.txt` file & `START_TIME`, `END_TIME` constants in `main.py` file to your needs
7. Run `python main.py`
