FROM python:3.8

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /code

COPY . /code

ENV PYTHONUNBUFFERED=1

ENTRYPOINT python3 app.py
