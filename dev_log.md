day 1:
1. created a virtual env , activated it and downloaded django , django rest framework, simplejwt , psycopg2-binary
2. Created a github rep ecommerce_backend
3. data base initialisation using sqlite. for now before actually creating postgre sql. created db.sqlite3 and applied migrations.
4. python manage.py runserver
   python manage.py createsuperuser
   user: hp
   pass: password
   emai: admin@example.com
5. in git
    * Initialized Git * Created proper .gitignore * Ignored: * venv/ * db.sqlite3 * **pycache**/ * .env * logs
    Added requirements.txt
    pip freeze > requirements.txt

    note: orm is object relation mapper which is used to talk to the db using python instead of sql
    eg:orm.objects()

day 2:
perform checks to ensure everything is done corectly until now


day 3:
create user models - for authentication to be more flexible , futureproof.
    django comes with a defualt user model but this uses userame to login but we want to use email , add unique email constraint and extensible profilelogic . If we stick onto default user then changing becomes very complicated later on . So we create custom user model.

    changing default user after migrations becomes very difficult

    steps:
    1. create accounts app
    python manage.py startapp accounts

    2.register app in settings -  in INSTALLED APP[]

    3.create custom user model in accounts/model.py

    4.tell django to use this model - in core/settings.py add AUTH_USER_MODEL

    5. Make migrations
        note: if migrations were made earlier we have to delete all that and also delete the dbsqlite3

        python manage.py makemigrations
        python manage.py migrate

    6. create superuser
        enter email, username and pass 
        eg: kripa@gmail.com , kripa , #kripa@2005

    7.register model in admin.py

    so far we have only till the admin panel and now
Django REST Framework (DRF) Integration - make a JSON based api server
    We now support:

    Frontend (React / Mobile) → Django API → JSON
    steps:
    1. install djangorestframework and add it to requirements.txt
    2. add rest_framework to installed apps and add to settings
    3. Add to views , create a simple test api endpoint
    4. wire
    5. run /api/health/

    result: api endpoint is wokring

Day 4:
serializers: for api validation and data conversion
converts python model to JSON and back and acts as a tranlations layer
there are two types of serialisers:
    1.Basic serializer: you manually write every fiels, it is more controlled and more work
    2.Model serializer: it builds fields automatically

two phases:
    1.validation phase
    2.creation of user phase
    password handling 

register engpoint:

JWT Authentication: It stands for JSON web tokens
until now we were using session authentication for login


