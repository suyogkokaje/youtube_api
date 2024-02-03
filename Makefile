worker:
	celery -A yt_api.celery worker -l info
beat:
	celery -A yt_api.celery beat --loglevel=info
postgresinit:
	sudo docker run --name assignment -p 5000:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=password -d postgres:15-alpine
postgres:
	sudo docker exec -it assignment psql
createdb:
	sudo docker exec -it assignment createdb --username=root --owner=root videos
dropdb:
	sudo docker exec -it assignment dropdb videos



.PHONY: worker beat