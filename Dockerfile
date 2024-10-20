FROM python:3.10

RUN apt-get update && \
    apt-get install -y libpq-dev build-essential postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app

CMD ["fastapi", "run", "app/backend.py", "--port", "3333", "--proxy-headers", "--workers", "4"]