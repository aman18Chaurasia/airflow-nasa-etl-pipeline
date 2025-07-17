# 🌌 NASA APOD ETL Pipeline with Apache Airflow(End to End)

This project is a production-ready ETL pipeline built using **Apache Airflow**. It extracts data from NASA's Astronomy Picture of the Day (APOD) API and stores it in a **PostgreSQL** database for further analysis or exploration.

## 📦 Project Structure

```
.
├── dags/                        # DAG definition for the ETL
├── include/                    # Extra scripts (if any)
├── plugins/                    # Custom Airflow plugins
├── tests/                      # DAG integrity tests
├── Dockerfile                  # Custom Astro runtime image
├── docker-compose.yml          # Local Airflow setup
├── airflow_settings.yaml       # Connections and variables config
├── requirements.txt            # Python dependencies
├── packages.txt                # OS-level packages
└── README.md
```

## 🚀 Features

- ⏰ **Daily scheduled DAG**
- 🔗 Connects to **NASA's APOD API** (via HTTP connection)
- 🧱 Transforms and validates the JSON response
- 🛢️ Loads the data into **PostgreSQL** using `PostgresHook`
- ⚙️ Uses Airflow best practices: decorators, catchup=False, task chaining

## 🔌 Airflow Connections Setup

1. **Postgres Connection**
   - **Conn ID**: `my_postgres_connection`
   - **Type**: `Postgres`
   - **Host**: `postgres`
   - **Schema**: `postgres`
   - **Login**: `postgres`
   - **Password**: `postgres`
   - **Port**: `5432`

2. **NASA API HTTP Connection**
   - **Conn ID**: `nasa_api`
   - **Type**: `Generic` (or use `HTTP` if available)
   - **Extra**:
     ```json
     {
       "api_key": "YOUR_NASA_API_KEY"
     }
     ```

## 📥 DAG Details

- **DAG ID**: `nasa_apod_postgres`
- **Schedule**: `@daily`
- **Tasks**:
  - `create_table()`: Initializes `apod_data` table
  - `extract_apod()`: Fetches JSON from NASA API
  - `transform_apod_data()`: Cleans and restructures the data
  - `load_data_to_postgres()`: Inserts into PostgreSQL with conflict handling

## 📦 Setup & Deployment

### Run Locally

```bash
# Start Airflow
astro dev start

# View UI at http://localhost:8080
# DAGs folder is auto-synced
```

### Deploy to Astronomer

```bash
astro deployment list
astro deploy
```

## 🧪 Testing

```bash
astro dev run pytest
```

## 🧾 Example Query

```sql
SELECT * FROM apod_data ORDER BY date DESC LIMIT 5;
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> Built with ❤️ by Aman Chaurasia
