FROM python:3.10.8
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN pip install -U pip

WORKDIR /watch-shop

COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY api_old /watch-shop

CMD ["python","manage.py","migrate"]