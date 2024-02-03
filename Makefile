worker:
	celery -A yt_api.celery worker -l info
beat:
	celery -A yt_api.celery beat --loglevel=info



.PHONY: worker beat