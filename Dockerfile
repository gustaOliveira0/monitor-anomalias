FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install pytest

# Permite escolher o comando na hora de rodar
ENTRYPOINT ["python"]
CMD ["main.py"]
