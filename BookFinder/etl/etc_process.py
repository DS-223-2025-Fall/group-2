import pandas as pd
import glob
import os
from os import path
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import logging
from Database.database import engine

logger = logging.getLogger(__name__)

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
        "url": "description"  # optional: store URL as description
    }

    df = df.rename(columns=column_mapping)
    
    # Keep only the columns that exist in the table
    df = df[list(column_mapping.values())]

    # Write to DB
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logger.info(f"Loaded data into table: {table_name}")


# -----------------------------------------------------
# Load CSV Data into Database Tables
# -----------------------------------------------------

folder_path = "data/*.csv"
files = glob.glob(folder_path)
files = sorted(files, key=os.path.getmtime)
base_names = [path.splitext(path.basename(file))[0] for file in files]

for table in base_names:
    try:
        logger.info(f"Loading data into table: {table}")
        load_csv_to_table(table, path.join("data/", f"{table}.csv"))
    except Exception as e:
        logger.error(f"Failed to ingest table {table}. Error: {e}")
        print(f"Failed to ingest table {table}. Moving to the next!")

print("Tables are populated.")
