FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

COPY requirements.txt .

RUN uv pip install --system --no-cache -r requirements.txt

COPY . .

