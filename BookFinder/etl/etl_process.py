import pandas as pd
import glob
import os
from os import path
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import logging
from database.database import engine, Base
from database.models import Book, AppUser, Bookstore, BookStoreInventory, BookSimilarity, SearchQuery, Ratings
from fastapi import status

# ➡️ New Imports for Web Service ⬅️
from fastapi import FastAPI, HTTPException
import uvicorn

# Configure logging (good practice for services)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
Base.metadata.create_all(engine)
# ➡️ Initialize FastAPI Application ⬅️
app = FastAPI()

# --- EXISTING ETL LOGIC FUNCTIONS ---

def load_csv_to_table(table_name: str, csv_path: str) -> None:
    """
    Load data from a CSV file into a database table.
    """
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT 1 FROM {table_name} LIMIT 1"))
        if result.first() is not None:
            logger.info(f"Table '{table_name}' already has data. Skipping CSV load.")
            return
        
    df = pd.read_csv(csv_path)
    # Write to DB
    df.to_sql(table_name, con=engine, if_exists="append", index=False, method="multi")
    logger.info(f"Loaded data into table: {table_name}")

# -----------------------------------------------------
# ➡️ New: FastAPI Endpoint to Trigger Data Load ⬅️
# -----------------------------------------------------

@app.post("/load_all_csv")
def trigger_data_ingestion():
    """
    Triggers the process to load all CSV files in the specified order.
    """
    logger.info("Starting data ingestion process via API trigger.")

    # Define explicit order of CSVs/tables
    table_order = [
        "bookstore",
        "book",
        "book_store_inventory",
    ]

    successful_tables = []
    failed_tables = {}

    for table in table_order:
        csv_path = f"data/{table}.csv"
        if not path.exists(csv_path):
            logger.warning(f"CSV file not found for table: {table}, skipping.")
            continue

        try:
            logger.info(f"Attempting to load data into table: {table}")
            load_csv_to_table(table, csv_path)
            successful_tables.append(table)
        except Exception as e:
            logger.error(f"Failed to ingest table {table}. Error: {e}")
            failed_tables[table] = str(e)

    if failed_tables:
        logger.error("Ingestion completed with failures.")
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