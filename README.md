# Youtube API

### **API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.**

<hr>

## Features

1. Multiple API keys can be added through admin dashboard or making post request to the following url  
   `http://127.0.0.1:8000/api/api-keys/`.

2. `Celery` is used to asynchronously fetch and store the data of the videos from youtube api.

3. `Redis` caching is implemented to cache the response of the page.

4. `PostreSQL` database is used to store the data. It is indexed on `published_at` field for faster sorting of data based on `published_at` field.

5. If quota of any of the API keys is exhausted then that key is blacklisted (can never be used again) and the next available API key will be used.

<hr>

## Tech Stack

- Django
- DRF
- Celery
- Redis
- PostgreSQL

<hr>

## How to run

1. Ensure that you have Python,PostgreSQL and Redis installed and you are on Linux OS.

2. Clone the repository

```bash
    git clone https://github.com/suyogkokaje/youtube_api.git
```

3. Enter in the root directory of the repository and create the virtual environment and activate it

```bash
    python3 -m venv env && source env/bin/activate
```

3. Create the .env file from .env.example file in the root of the project

```bash
    cp .env .env.example
```

4. Generate the secret key for your app and update it in the .env file

```bash
    # Open a Python shell
    python backend/manage.py shell

    >> from django.core.management.utils import get_random_secret_key
    >> get_random_secret_key()

```

5. Apply database migrations

```bash
    python manage.py makemigrations && python manage.py migrate
```

5. Create a super user to add API keys in the database using admin dashboard

```bash
    python manage.py createsuperuser
```

6. Now add the API keys to the database. Visit the admin dashboard on below url

```bash
    http://127.0.0.1:8000/admin
```

7. Now to run the project open 3 different terminals and enter each of the belowcommand in different terminals to run the application, celery worker and celery beat respectively.

```bash
    python manage.py runserver
```

```bash
    celery -A yt_api.celery worker -l info
```

```bash
    celery -A yt_api.celery beat --loglevel=info
```

8. Now to retrieve the data stored in the database you can make the `GET` request to the following url

```bash
    http://127.0.0.1:8000/api/videos/
```

9. To view the documentation visit the below url

```bash
    http://127.0.0.1:8000/swagger/
```