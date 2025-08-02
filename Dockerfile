FROM python:3.11-slim
WORKDIR /app

RUN apt update && apt install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mt/ ./mt

EXPOSE 8080
CMD ["python", "-m", "mt.server"]
