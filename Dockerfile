FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 0.0.0.0 listens on all container interfaces so the host can reach the API through the published port.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]