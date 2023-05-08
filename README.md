# api_yamdb. Now dockerized!

![yamdb workflow](https://github.com/frrenzy/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Description

REST API for cinema/books/music database.
Documentation is available at [/redoc](http://localhost/redoc)

### Try it out

Project available [here](80.78.255.252)

### Local development

1. Clone this repo

2. Go to `infra` directory

```sh
cd infra
```

3. Fill `.env` with your data as in `.env.example`
4. Run these commands

```sh
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
```

5. Import some fixture data into database

```sh
docker-compose exec web python manage.py import Category Genre Title GenreTitle User Review Comment

```

or

```sh
docker-compose exec web django-admin loaddata fixtures.json
```

6. Enjoy!

### Author

[Ivan Sizov](https://github.com/frrenzy)
