FROM python:3.10

WORKDIR /code

COPY ./requirements-fastapi.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "3333", "--proxy-headers", "--workers", "4"]