# Watch-shop with in Docker environment with Backend(DRF), Frontend(NuxtJS), Nginx, PostgreSQL.

### Built with

* ![Docker][Docker]
* ![Django][Django]
* ![Nginx][Nginx]
* ![Gunicorn][Gunicorn]
* ![PostgreSQL][PostgreSQL]
* ![NuxtJS][NuxtJS]
* ![Yookassa][Yookassa]

## Features
* Get token using simple-jwt after authentication.
* Products
* Add products to cart.
* Delete products to cart.
* Create payment to orders in the Cart.
* Payment system: Yookassa.
* Review to product
* Feedback to shop
* News blog
* Like news
* Comment news

## Endopints
To get information about endoints, open the [endoints.yaml](https://github.com/tema1998/DRF-watch-shop/blob/master/endpoints.yaml).

Or use the next links:

[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

[http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)


## Frontend(NuxtJS)
![Index](/readme_files/frontend1.png)
![Cart](/readme_files/frontend2.png)
![Payment](/readme_files/frontend3.png)

## Config file
Create .env using .env.example.

## Yookassa settings
Create an account [https://yookassa.ru/yooid/signup/](https://yookassa.ru/yooid/signup/).
In the http events notification turn on only 'payment.succeeded' and 'payment.canceled'.
In .env file, set your yookassa account data.
```
YOOKASSA_ACCOUNT_ID=yookassa_account_id
YOOKASSA_SECRET_KEY=yookassa_secret_key
```

## Run docker
```
docker build -t watch_project ./api/ --no-cache
docker build -t frontend_watch ./frontend/ --no-cache
docker-compose up --build
```
## Stop:
```
docker stop $(docker ps -q)
```


[Docker]: https://img.shields.io/badge/docker-000000?style=for-the-badge&logo=docker&logoColor=blue
[Django]: https://img.shields.io/badge/django-000000?style=for-the-badge&logo=django&logoColor=white
[PostgreSQL]: https://img.shields.io/badge/postgresql-000000?style=for-the-badge&logo=postgresql&logoColor=blue
[Gunicorn]: https://img.shields.io/badge/gunicorn-000000?style=for-the-badge&logo=gunicorn&logoColor
[Nginx]: https://img.shields.io/badge/nginx-000000?style=for-the-badge&logo=nginx&logoColor=green
[NuxtJS]: https://img.shields.io/badge/nuxtjs-000000?style=for-the-badge&logo=javascript&logoColor
[Yookassa]: https://img.shields.io/badge/yookassa-000000?style=for-the-badge&logo=yookassa&logoColor
