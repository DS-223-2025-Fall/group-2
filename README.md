# BookFinder Deployment

This project is deployed on Azure Kubernetes Service (AKS).

You can access the different parts of the system as follows:

- **Frontend (User Interface)**  
  View the live frontend here: [https://bookfinder.swedencentral.cloudapp.azure.com](https://bookfinder.swedencentral.cloudapp.azure.com)

- **API (FastAPI backend)**  
  Access the API documentation (Swagger UI) here: [https://bookfinder.swedencentral.cloudapp.azure.com/api/docs](https://bookfinder.swedencentral.cloudapp.azure.com/api/docs)

- **PGAdmin (Database Management)**  
  Access PGAdmin here: [https://bookfinder.swedencentral.cloudapp.azure.com/pgadmin](https://bookfinder.swedencentral.cloudapp.azure.com/pgadmin) (Credentials not provided)

---

# Dockerized ETL, PostgreSQL, pgAdmin, Backend Setup, Streamlit Setup

## Branches

This repository contains the following branches:

- **main**: The primary branch containing the complete project setup.
- **gh-pages:** Deploying the documentation.

## Installation

1. Clone the repository:
   ```bash
   git clone hhttps://github.com/DS-223-2025-Fall/group-2.git
   cd BookFinder
   ```

2. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

## Access the Application

After running `docker-compose up --build`, you can access each component of the application at the following URLs:

- **Streamlit Frontend:** http://localhost:8501 The main interface for discovering, searching, and rating books.
- **FastAPI Backend**: [http://localhost:8008](http://localhost:8008)  
  The backend API where requests are processed. You can use tools like [Swagger UI](http://localhost:8008/api/docs) (provided by FastAPI) to explore the API endpoints and their details.
- **PgAdmin** (optional): [http://localhost:5050](http://localhost:5050)  
  A graphical tool for PostgreSQL, which allows you to view and manage the database. Login using the credentials set in the `.env` file:
- **Documentation (MkDocs)** : [https://ds-223-2025-fall.github.io/group-2/](https://ds-223-2025-fall.github.io/group-2/)  
  Full project documentation including backend, frontend, ETL, and data science modules.

> Note: Ensure Docker is running, and all environment variables in `.env` are correctly configured before accessing these URLs.

## Project Structure

Here’s an overview of the project’s file structure:

```bash
.
BookFinder/
├── backend/
│   ├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── app.py
│   ├── components/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── etl/
│   ├── data/
│   ├── database/
│   ├── etl_process.py
│   ├── Dockerfile
│   └── requirements.txt
├── kube/
│   └── ... (Kubernetes deployment and service files)
└── scraping
│   ├── books.am_scraping.py
│   ├── requirements.txt
│   └── zangak_scraping.py
├── docker-compose.yml
├── README.md
├── docs/
└── venv/
```

## Docker

This repository provides a complete Docker-based development environment with **five main services**:

1. **Frontend (Streamlit):** - main interface
![D1](docs/img/docker_front.png)

2. **Backend (FastAPI):** - powers the API logic.  
![D2](docs/img/docker_back.png)

3. **PostgreSQL (db):** - persistent database storage.  
![D3](docs/img/docker_db.png)

4. **pgAdmin:** - browser-based UI for managing PostgreSQL.  
![D4](docs/img/docker_pgadmin.png)

5. **ETL Service:** - A Python-based ETL component for Extract–Transform–Load operations.  
![D5](docs/img/docker_etl.png)

### Volumes

Two Docker volumes are created automatically:

- **postgres_data** – persists PostgreSQL database files  
- **pgadmin_data** – persists pgAdmin configuration



## Prerequisites

Before running this setup, ensure Docker and Docker Compose are installed on your system.


- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)


## DB

- Access pgAdmin for PostgreSQL management: [http://localhost:5050](http://localhost:5050)
    - username: admin@admin.com 
    - password: admin
    - When running for the first time, you must create a server. Configure it as shown in the below image (Password is blurred it should be `password`.)


## ETL

### Schema Design

We will try to create below schema:

![Star Schema](docs/img/ERD.png)

In `models.py`, we have used `sqlalchemy` package, which allows map python objects with SQL objects.

By running `etl.py` following objects will be created:
    - sql tables 
    - the data sets will store in `data\` folder
    - the csv files will be loaded into DB

## API

![Swagger_1](docs/img/Swagger_1.png)
![Swagger_2](docs/img/Swagger_2.png)


## Web Application

To Open the web app visit: [here](http://localhost:8501/)

![UI_1](docs/img/Home_page.png)
![UI_2](docs/img/Search_results.png)
![UI_3](docs/img/Search_results_similars.png)
![UI_4](docs/img/Login_page.png)
