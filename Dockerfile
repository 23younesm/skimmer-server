FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py webapp.py ./
COPY templates ./templates
COPY static ./static

RUN mkdir -p /data && echo '[]' > /data/creds.json

EXPOSE 9999 8080

CMD ["sh", "-c", "python -u server.py & python -u webapp.py"]
