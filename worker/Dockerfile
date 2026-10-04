FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY worker.py .
COPY tests ./tests
FROM base AS test
CMD ["pytest", "-q"]
FROM python:3.12-slim AS production
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY worker.py .
RUN useradd --create-home --uid 10002 worker && chown -R worker:worker /app
USER worker
CMD ["python", "worker.py"]

