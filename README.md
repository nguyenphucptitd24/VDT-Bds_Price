# 🏙️ End-to-End Real Estate Data Pipeline: Vinhomes Smart City

## 📖 Overview

This project is an End-to-End Data Engineering pipeline designed to automatically extract, process, load, and visualize real estate data (specifically for the Vinhomes Smart City area).

The primary objective is to build a robust ETL (Extract, Transform, Load) workflow that converts raw, semi-structured API data into a clean, tabular format stored in a Cloud Data Warehouse, ultimately serving an interactive analytical dashboard.

## 🛠️ Tech Stack & Architecture

This project adheres to a standard ETL architecture:

- **Core Language:** Python 3.x
- **Extract (Ingestion):** `requests`, `json` (RESTful API interaction, pagination handling, rate-limiting).
- **Transform (Processing):** `pandas` (Vectorization, Type Casting, Missing Value Handling, Schema Standardization).
- **Load (Storage):** `sqlalchemy`, `psycopg2-binary` (Data ingestion to **Supabase PostgreSQL** Serverless Database).
- **Data Visualization:** `streamlit` (Interactive Web App and Dashboarding).

## 🚀 Pipeline Phases

### Phase 1: Data Ingestion (`extract.py`)

- Establishes a connection to a public real estate API to fetch the latest property listings.
- Implements defensive programming to handle pagination offsets and HTTP headers.
- Outputs the raw semi-structured data into an intermediate standard format (`vinhomes_smart_city_listings.json`).

### Phase 2: Data Transformation (`transform.py`)

- Loads raw data into a Pandas DataFrame for vectorized batch processing.
- **Data Cleansing:** Performs dimensionality reduction by dropping over 90 noisy, irrelevant columns.
- **Data Integrity:** Resolves schema conflicts (e.g., mapping the correct area size from ambiguous API fields).
- **Type Casting & Filtering:** Casts string formats to numeric data types and drops records with `NaN` values in critical fields (Price, Area).
- Outputs the processed data as `vinhomes_clean.csv`.

### Phase 3: Cloud Loading (`load.py`)

- Configures a database engine to connect with a Serverless PostgreSQL database (Supabase).
- Loads the cleaned dataset into the cloud storage, making it highly available for OLAP queries and BI tools.

### Phase 4: Data Visualization (`app.py`)

- Initializes a Streamlit Web Application.
- Fetches live data directly from the Supabase Cloud Database.
- Renders interactive data visualizations, including price distribution bar charts and a cleaned data matrix.

## 💡 How to Run Locally

To set up and run the entire pipeline, execute the following commands sequentially in your terminal:

```bash
# 1. Clone the repository and navigate to the directory
git clone [https://github.com/your-username/vdt-real-estate-pipeline.git](https://github.com/your-username/vdt-real-estate-pipeline.git)
cd vdt-real-estate-pipeline

# 2. Install dependencies
pip install pandas requests sqlalchemy psycopg2-binary streamlit

# 3. Execute the ETL Pipeline
python extract.py     # Step 1: Ingest raw data
python transform.py   # Step 2: Clean and transform data
python load.py        # Step 3: Load data to Cloud (Remember to configure your DB_URI in the script first)

# 4. Launch the Dashboard
streamlit run app.py

Author: Nguyen Hong Phuc
```
