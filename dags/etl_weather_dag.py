from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import json

# Fungsi untuk mengambil data cuaca
def fetch_weather_data():
    api_key = "182e6c0694544665b52105141240312"
    city = "Jakarta"
    url = f"http://api.weatherapi.com/v1/current.json?key{api_key}&q={city}"
    response = requests.get(url)
    data = response.json()
    
    # Simpan ke file sementara
    with open('/tmp/weather_data.json', 'w') as f:
        json.dump(data, f)

# Fungsi untuk membersihkan data
def clean_weather_data():
    with open('/tmp/weather_data.json', 'r') as f:
        data = json.load(f)
    cleaned_data = {
        "city": data["location"]["name"],
        "temperature": data["current"]["temp_c"],
        "weather": data["current"][0]["description"]
    }
    
    # Simpan data bersih
    with open('/tmp/cleaned_weather_data.json', 'w') as f:
        json.dump(cleaned_data, f)

# Konfigurasi DAG
default_args = {
    'start_date': datetime(2024, 12, 1),
    'catchup': False
}

with DAG(
    dag_id="etl_weather_dag",
    default_args=default_args,
    schedule_interval="@daily",
    description="ETL pipeline for weather data"
) as dag:
    fetch_data = PythonOperator(
        task_id="fetch_weather_data",
        python_callable=fetch_weather_data
    )

    clean_data = PythonOperator(
        task_id="clean_weather_data",
        python_callable=clean_weather_data
    )

    fetch_data >> clean_data
