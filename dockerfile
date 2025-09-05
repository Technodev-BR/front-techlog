FROM python:3.11.4-slim

RUN apt-get update && apt-get install -y \
    iputils-ping \
    telnet \
    curl \
    apt-transport-https \
    gnupg2 \
    unixodbc-dev \
    gcc \
    g++ \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && apt-get install libzbar-dev -y
  
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY ./website /website
COPY ./entrypoint.sh /scripts

WORKDIR /website

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install numpy &&\
    /venv/bin/pip install pyzbar &&\
    /venv/bin/pip install -r /website/requirements.txt && \
    chmod -R +x /scripts
    
    
ENV PATH="/scripts:/venv/bin:$PATH"

EXPOSE 5000

CMD ["entrypoint.sh"]