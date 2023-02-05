## Set Up:
You need:

Python 3.10.6

NodeJS v18.13.0

`pip install -r requerements.txt`

`yarn`
** **


## Running app

<code> `python manage.py migrate` </code>

1. `python -m celery -A application worker -B -l INFO`

2. `yarn build`
3. `python manage.py createsuperuser --username=admin`
4. `python manage.py runserver`

Go to http://localhost:8000/admin and create some categories and products


