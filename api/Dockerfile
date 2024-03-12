FROM python:3.10.8
EXPOSE 8000

WORKDIR /watch-shop

RUN pip install -U pip

COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . /watch-shop

CMD ["python","manage.py","runserver"]