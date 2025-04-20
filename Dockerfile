FROM python:3.13-slim

WORKDIR /app

COPY . /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install pytest

CMD ["python", "main.py"]
