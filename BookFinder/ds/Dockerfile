FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY ./app /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python books.py"]
