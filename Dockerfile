FROM python:3.10.8
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev gunicorn &&\
  apt-get install --no-install-recommends -y wget make wait-for-it\
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /watch-shop
COPY requirements.txt ./
COPY /start.sh ./
COPY /.env ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY backend /watch-shop/

CMD ["/bin/bash", "start.sh"]
