# FROM python:3.11-slim-buster
FROM docker-registry.dp.nlmk.com/python:3.11-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN rm -rf /etc/apt/sources.list.d/* \
    && echo 'deb https://repos.dp.nlmk.com/artifactory/debian-remote bookworm main' > /etc/apt/sources.list \
    && apt -o "Acquire::https::Verify-Peer=false" update \
    && apt -o "Acquire::https::Verify-Peer=false" install -y ca-certificates
# RUN apt-get update && apt-get install -y libaio1  python3-dev python-dev && apt install nano


WORKDIR /backend
COPY ./requirements.txt /backend/

RUN python -m pip install --upgrade pip

RUN pip install -r /backend/requirements.txt

COPY . /backend/

# Основной скрипт
ENTRYPOINT ["python", "main.py"]

# Аварийный скрипт
# ENTRYPOINT ["python", "emergency_stop.py"]