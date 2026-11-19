FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY script.py .

ENV PYTHONUNBUFFERED=1
ENV CONCURRENT_WORKERS=30
ENV TOTAL_TASKS=500
ENV WAIT_TIME=5

CMD ["python", "script.py"]
