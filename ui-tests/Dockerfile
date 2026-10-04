FROM python:3.12-slim

WORKDIR /tests
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY test_ui.py .

RUN useradd --create-home --uid 10003 uitester && chown -R uitester:uitester /tests
USER uitester

CMD ["pytest", "-q"]
