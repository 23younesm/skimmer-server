FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server.py .
COPY webapp.py .
COPY templates ./templates

EXPOSE 9999 8080

CMD ["sh", "-c", "python server.py & python webapp.py"]
