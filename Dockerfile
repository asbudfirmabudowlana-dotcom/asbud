FROM python:3.13-slim

WORKDIR /workspace/apps/api

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY apps/api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# The API serves the Polish web application itself, so Railway needs only one web service.
COPY apps/api/app ./app
COPY apps/web/public ../web/public

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
