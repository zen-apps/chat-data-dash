FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install flask gunicorn && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt 

WORKDIR /opt/app

COPY ./dash_app /opt/app

ENV PYTHONUNBUFFERED=1

EXPOSE 8000
ENV PYTHONUNBUFFERED=True 
ENV PYTHONPATH=/app/app

CMD exec gunicorn --bind :8080 --log-level info --workers 1 --threads 8 --timeout 0 app:server




