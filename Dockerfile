FROM python:3.9.17-slim

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PIP_DISABLE_PIP_VERSION_CHECK=TRUE
ENV TOKENIZERS_PARALLELISM=TRUE

RUN apt-get update && apt-get install -y \
    build-essential

RUN pip install --upgrade pip setuptools

RUN useradd -ms /bin/bash chat
WORKDIR /home/code


COPY requirements.txt /home/code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/code/

ENV HOME /home
ENV PATH="/home/.local/bin:${PATH}"
ENV PYTHONPATH /home/code/src
RUN chown -R chat /home/code

RUN mkdir -p /home/.cache
RUN mkdir -p /home/.config

RUN chmod -R 777 /home/.cache
RUN chmod -R 777 /home/.config


USER chat