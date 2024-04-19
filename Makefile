make_migr:
	docker-compose run --rm django sh -c "python manage.py makemigrations"
migr:
	docker-compose run --rm django sh -c "python manage.py migrate"
test:
	docker-compose run --rm django sh -c "python manage.py test"
super:
	docker-compose run --rm django sh -c "python manage.py createsuperuser"
shell:
	docker-compose run --rm django sh -c "python manage.py shell"