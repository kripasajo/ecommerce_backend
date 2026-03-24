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
    steps:
        1. create serializers.py
            this creates the data validation+tranformation layer
            it defines what fields are allowed and required, how to create user properly , hash password safely
        2. create register view
            This connects:
            Incoming HTTP request → Serializer → Database → HTTP response
            - we ccheck is valid and if it is then we save the user
        3. wire the url route
            URL → View → Serializer → Model → Database
            it defines the url that has to be visted to run something

        4. testing: 
        admin registration successful . 
register endpoint:
we went to /api/register and we registred a new user using email , username , password

Implement Login:
Authenticate existing user using Django’s authentication system.
steps:
    1. add login view
    2. wire url
    3. tested

JWT Authentication: It stands for JSON web tokens
until now we were using session authentication for login

what is json?
    JWT (JSON Web Token) authentication is a secure, stateless, and compact method for transmitting user information between a client and a server. After logging in, the server issues a digitally signed token (JWT) to the client, which is sent with subsequent requests to verify identity and authorization, eliminating the need for server-side session storage.

    
Day 5 - 24/03/26

    1️ Install SimpleJWT
        pip install djangorestframework-simplejwt
        This gives us:
            Token generation
            Token validation
            Refresh mechanism
            Integration with DRF
    2️ Configure DRF to use JWT authentication
        In settings.py we will replace SessionAuthentication with JWTAuthentication
    3️ Replace manual login with JWT token endpoint
        we use ready made drf jwt-view TokenObtainPairView
        This view will:
            Authenticate user (just like your login)
            If correct → generate tokens
            Return:
                Access Token
                    Short-lived (e.g., 5–60 mins)
                    Used to access protected APIs
                    Sent in every request
                Refresh Token
                    Long-lived (e.g., days)
                    Used to get a new access token
                    Not used for normal API calls
        go to http://127.0.0.1:8000/api/token/
        enter username and password and then what happened
            Authenticated your user
            Generated JWT tokens
            Embedded your user ID inside the token
            Returned access + refresh tokens
    4️ Protect endpoints using IsAuthenticated
        Open accounts/views.py Modify your health check:
    5️ Test access with and without token
        without: "detail": "Authentication credentials were not provided."
        with:
        Thunder Client simulates a real API consumer
        Login → Get Token → Use Token → Access Protected API
            Thunder Client is used in the “Use Token” step
        steps:
        install thundercleint , create a new request , in get add /api/health/ link , add header authorization and add Bearer <access_token> , then send request and we will see an ok .

🛡 2. Protect Endpoints

Switch default permission to IsAuthenticated
    Before this every api was public unless protected manually . After this every API is protected by default and you must explicity allow public ones
Protect specific routes
    to open only specific routes
Test unauthorized access

🔄 3. Refresh Token Endpoint
Allow users to stay logged in without re-entering password
Implement token refresh
Test refresh lifecycle

📦 4. Optional (Clean Auth Architecture)

Separate auth/ URLs

Modular URL configuration

Improve response structure




