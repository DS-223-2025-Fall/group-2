import pandas as pd
import glob
import os
from os import path
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import logging
from database.database import engine
from fastapi import status

# ➡️ New Imports for Web Service ⬅️
from fastapi import FastAPI, HTTPException
import uvicorn

# Configure logging (good practice for services)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ➡️ Initialize FastAPI Application ⬅️
app = FastAPI()

# --- EXISTING ETL LOGIC FUNCTIONS ---

def load_csv_to_table(table_name: str, csv_path: str) -> None:
    """
    Load data from a CSV file into a database table.
    """
    df = pd.read_csv(csv_path)
    
    # Map CSV columns to DB table columns
    column_mapping = {
        "ISBN": "isbn",
        "title": "title",
        "author": "author",
        "genre": "genre",
        "language": "language",
        "data_source": "data_source",
        "url": "description"
    }

    df = df.rename(columns=column_mapping)
    
    # Keep only the columns that exist in the table
    # Note: Using try/except here is more robust if a column is missing
    db_cols = list(column_mapping.values())
    df = df.reindex(columns=db_cols) 

    # Write to DB
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logger.info(f"Loaded data into table: {table_name}")

# -----------------------------------------------------
# ➡️ New: FastAPI Endpoint to Trigger Data Load ⬅️
# -----------------------------------------------------

@app.post("/load_all_csv")
def trigger_data_ingestion():
    """
    Triggers the process to load all CSV files in the 'data/' folder to the database.
    """
    logger.info("Starting data ingestion process via API trigger.")
    
    folder_path = "data/*.csv"
    files = glob.glob(folder_path)
    files = sorted(files, key=os.path.getmtime)
    base_names = [path.splitext(path.basename(file))[0] for file in files]
    
    successful_tables = []
    failed_tables = {}

    for table in base_names:
        try:
            logger.info(f"Attempting to load data into table: {table}")
            load_csv_to_table(table, path.join("data/", f"{table}.csv"))
            successful_tables.append(table)
        except Exception as e:
            logger.error(f"Failed to ingest table {table}. Error: {e}")
            failed_tables[table] = str(e)

    if failed_tables:
        logger.error(f"Ingestion completed with failures.")
        # Return a 500 status if any table failed to load
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Tables are populated with some failures.",
                "successful_tables": successful_tables,
                "failed_tables": failed_tables
            }
        )
    
    logger.info("Tables are fully populated.")
    return {"message": "Tables are fully populated.", "successful_tables": successful_tables}

# -----------------------------------------------------
# ➡️ Running the Server on Port 3000 ⬅️
# -----------------------------------------------------
@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    """
    Kubernetes and Load Balancer health check endpoint.
    Returns 200 OK if the server is running.
    """
    return {"status": "ok", "service": "etl-service"}

# ➡️ CHANGE: Define the startup function using the decorator ⬅️
@app.on_event("startup")
def startup_event():
    """
    Runs the initial ETL load when the application starts up.
    """
    logger.info("Application startup event triggered. Starting initial data ingestion.")
    # Call your data loading function directly
    trigger_data_ingestion()
    logger.info("Initial data ingestion complete.")

if __name__ == "__main__":
    # ⚠️ This is the command that makes the script "listen to port 3000"
    uvicorn.run(app, host="0.0.0.0", port=3000)