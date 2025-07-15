from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
from airflow.hooks.base import BaseHook
import requests

# DAG definition
with DAG(
    dag_id='nasa_apod_postgres',
    start_date=datetime.now() - timedelta(days=1),
    schedule='@daily',
    catchup=False,
    tags=['nasa', 'apod', 'etl']
) as dag:

    # Step 1: Create table
    @task
    def create_table():
        create_table_query = """
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE UNIQUE,
            media_type VARCHAR(50)
        );
        """
        hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        hook.run(create_table_query)
        print("✅ Table created or already exists.")

    # Step 2: Extract data using requests
    @task
    def extract_apod() -> dict:
        conn = BaseHook.get_connection("nasa_api")
        api_key = conn.extra_dejson.get("api_key")
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
        
        response = requests.get(url)
        response.raise_for_status()
        print("✅ APOD data fetched.")
        return response.json()

    # Step 3: Transform
    @task
    def transform_apod_data(response: dict) -> dict:
        transformed = {
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),
            'media_type': response.get('media_type', 'unknown')
        }
        print("✅ Data transformed.")
        return transformed

    # Step 4:  Load to PostgreSQL
    @task
    def load_data_to_postgres(apod_data: dict):
        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (date) DO NOTHING;
        """
        hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        hook.run(
            insert_query,
            parameters=(
                apod_data['title'],
                apod_data['explanation'],
                apod_data['url'],
                apod_data['date'],
                apod_data['media_type']
            )
        )
        print(f"✅ Data for {apod_data['date']} inserted.")

    # DAG pipeline
    create = create_table()
    raw = extract_apod()
    transformed = transform_apod_data(raw)
    loaded = load_data_to_postgres(transformed)

    create >> raw >> transformed >> loaded
