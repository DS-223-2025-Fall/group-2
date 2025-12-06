# BookFinder Documentation

Welcome to the BookFinder project documentation. This project is a full-stack application that helps users discover, search, and rate books, integrating backend, frontend, and ETL components, with Kubernetes deployment and Docker support.

## Project Structure Overview 

The main folders and files are structured as follows:

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
├── scraping/
│   └── requirements.txt
├── docker-compose.yml
├── README.md
├── docs/
└── venv/
```

36 directories, 103 files
---

## Documentation Sections

### Problem Definition
- **[Problem Definition](problem_definition/index.md)**  
  Explains the challenges that BookFinder addresses, project objectives, and overall scope.

### Backend
- **[Backend](backend.md)**  
  Covers backend architecture, API endpoints, database models, deployment instructions, and Docker integration.

### Frontend
- **[Frontend](frontend.md)**  
    The frontend is built with Streamlit and consists of multiple reusable components, each handling a specific part of the user interface. Users can search for books, view book details, log in, and submit or browse ratings seamlessly. The main components include: authentication, book cards, detailed book pages, the home page, login page, rating widget, and search results display.
### ETL
- **[ETL](etl.md)**  
  Details the extraction, transformation, and loading processes, including database initialization, data pipelines, and automated ETL tasks.

### Data Science
- **[Data Science](data_science.md)**  
  Explains data processing, recommendation algorithms, analytics, and other computational components.

---

## Media & Images

The `docs/img/` directory contains visuals, including:  

- **Backend.png** – Backend architecture diagram  
- **ERD.png** – Database entity relationship diagram  
- **UI1.png**, **UI2.png**, **UI3.png** – Frontend UI screenshots  

---

This documentation is generated using **MkDocs** and includes automatically extracted Python API documentation via **mkdocstrings**. Navigate through the sections to explore the architecture, functionality, and implementation details of BookFinder.
