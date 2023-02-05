# Set Up:
Python >= 3.10.6

NodeJS v18.13.0

<br>

# Install deps
### 1. Back-end
```bash
pip install -r requerements.txt
```
### 2. Front-end
```bash
yarn
```
<br>

# Running app

### 1. Migrations
```bash
python manage.py migrate
```
### 2. Celery
```bash
python -m celery -A application worker -B -l INFO
```
### 3. Building front-end
```bash
yarn build
```
### 4. Create user
```bash
python manage.py createsuperuser --username=admin
```
### 5. Get staticfiles
```bash
python manage.py collectstatic
```
### 6. Run server
```bash
python manage.py runserver --nostatic
```

### ...or just run
```bash
python manage.py runserver --insecure
```
instead of 5 and 6
<br>
<br>
<br>

Go to http://localhost:8000/admin and create some categories and products

Also you can create local_settings file with specific db:

```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'qrgenerator',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 0
    }
}
```
PS: You also need to install psycopg2 via pip and some libraries for PostgreSQL

Or you can use sqlite db =)