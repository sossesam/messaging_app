FROM python:3.10 AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /messaging_app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt


FROM base AS dev

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
    
COPY . /messaging_app 
RUN pip install --no-cache-dir pytest
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS prod
COPY . /messaging_app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "messaging_app.wsgi:application"]


