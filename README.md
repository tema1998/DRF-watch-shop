# Watch-shop with in Docker environment with Backend(DRF), Frontend(NuxtJS), Nginx, PostgreSQL.

### Built with

* ![Docker][Docker]
* ![Django][Django]
* ![Nginx][Nginx]
* ![Gunicorn][Gunicorn]
* ![PostgreSQL][PostgreSQL]
* ![NuxtJS][NuxtJS]


## Structure
Backend(DRF) contains the following endpoints:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`api/products/` | GET | READ | Get all products(with pagination)
`api/products/slug/` | GET | READ | Get product by slug
`api/products/?search=key` | GET | READ | Find products by key(with pagination)
`api/profile/` | GET | READ | Get info about user profile
`api/reviews/slug/` | GET | READ | Get reviews for product by product slug
`api/reviews/`| POST | CREATE | Create a review
`api/feedback/`| POST | CREATE | Write feedback to admin email
`api/register/`| POST | CREATE | Register
`api/token/`| POST | CREATE | Get "refresh" and "access" tokens
`api/refresh_token/`| POST | CREATE | Get new "access" token (refresh)
`New functions will be added later.`|  |  | 



Functions 'Follow/unfollow', 'Like/dislike', 'Add posts to favorites' implemented using **JS**(*without page refresh*).

## Config file
Create .env, set your data.
```
POSTGRES_ENGINE = django.db.backends.postgresql
POSTGRES_HOST=pgdb
POSTGRES_PORT=5432
POSTGRES_USER=pguser
POSTGRES_PASSWORD=password
POSTGRES_DB=mydb
DJANGO_DEVELOPMENT=0
DJANGO_SETTINGS_MODULE="api.settings"
SECRET_KEY=your_secret_key
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
