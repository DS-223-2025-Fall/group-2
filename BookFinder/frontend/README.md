## Running the Frontend
### Run Locally (without Docker)

Make sure you have Python 3.10+ installed.
```
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## Dockerfile Summary

The Dockerfile:

- Uses `python:3.11-slim`
- Installs all dependencies from `requirements.txt`
- Copies the Streamlit app into `/app`
- Runs the app on port `8501`
