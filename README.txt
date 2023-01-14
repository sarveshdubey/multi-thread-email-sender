MULTI-THREADING eMAIL SENDER

This is a python-django based application which sends emails to all the subscribers present in the database.
The process runs in the background and uses multithreading.

STEPS and REQUIREMENTS:
python --version == 3.10.7
django-version == 4.1.3
Module requirements -> run "pip install -r requirements.txt"

Fill the email details in the .env file (Note - do not add any kind of inverted commas while adding username and password)

run commands:

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

Endpoints:
/sub/ == Subscribes and adds user to the database.
/api/ == Takes an optional argument 'threads', which is the desired number of threads the user wants to run.
Default number is the product of number of cores present in the CPU and 5.
The API creates a log of every thread in 'logs.log' file