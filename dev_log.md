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

📦 4. Optional (Clean Auth Architecture)  // not done
Separate auth/ URLs
Modular URL configuration
Improve response structure

Day 6: 25/03/2026
Phase 2: User → Product → Cart → Order
🧩 Core Systems
 Product & Category system
    1. create a mew app python manage.py startapp products -> we got products folder
    2. register the model  in core/setting in the installed apps
    3.in products/models
    ActiveManager model: handles queries - controls how data is retrieved
        -implemented a custom model manager to automatically exclude soft-deleted records from queries, improving code cleanliness and reducing repetition.
    Base model: handles fields
        -is_deleted: it's added here so all models will get it
        - we get timestamps
    category model:
        -parent → supports hierarchy
        -indexes → faster queries (INTERVIEW GOLD)
        -is_active → soft-disable categories
        -unique category name
        -on_delete=models.PROTECT instead of CASCADE:used PROTECT to ensure referential integrity and prevent accidental deletion of dependent records.
        -soft delete pattern
        -slug index
        -added database indexes on frequently queried fields like slug and parent in the Category model to improve query performance, especially for hierarchical queries
    product model:
        -slug: SEO + API friendly
    4. in products/views
        
    5. in products/serializers-for drf to process requests
    - Converts your Django models → JSON (API response)
    -Converts JSON → model (when creating product)
    -excluded is_delted as users should not control deletion
    6. Run migrations after creating models
    7. Register in admin panel
    8. Add Filtering + Search + Ordering
        intsall django-filter
        update view
    9. in products/urls.py
        connect to core/urls.py
    10.Add category API and pagination
        pagination is needed for scalbility
Day 7: 26/03/2026
    11. Test using DRF UI
    -create category
    -create product
    -test filters
    -search
    -sort
    -soft deleted test
    all tests pass
 Product Variants
1.CREATE ProductVariant MODEL
    -foreign key: one-to-many relationship to support multiple configurations per product
    -related_name='variants': Used related_name for reverse querying and cleaner ORM access.
    -size and color: Chose a structured approach instead of dynamic attributes to keep the system simple and scalable.
    -price with vaalidator:
    -stock'
    -sku
    -indexes
    -unique constraint
    -__str__
    2.Run migrations
    3.Register with admin
2.serializers
    -Add serialisers
    -Add validation in serializer: Serializer validation provides immediate user-friendly API errors, while model validation ensures database-level integrity.
3.views
4.urls
5.tests
6.nested varinats: used nested serializers to include product variants within product responses to reduce API calls and improve performance
7.select_related/prefetch_related:optimized queries using prefetch_related to avoid N+1 query problems.”

day 8: 31/3/26
  Cart system (User → Cart → CartItem → ProductVariant)
Models
Migrations
Serializer:
 cartitemserializer with validation: so it shows can't add more items than stock from cart to prevent overselling
 -productvarinat and productvariantid: seperates read and write representatons to provide detailed reponses while keeping input simple
 cartserializer: api returns full cart. items, totalprice-SerializerMethodField to dynamically compute total cart value
Views
abstracted business logic into a service layer to improve maintainability and scalability
- only logged in users can access cart
-user can only modify their cart
-view->service->model
URLs
Testing


Day 9: 1/4/2026
 Order system (basic)
1.Model
  -Order 
  -OrderItem
2.Relationships
 order-> many orderitems
 many orderitem->one product variant

3.serializers
orderitemserializer
orderserializer
    nestedproductinfo
    orderitem is read only
    view->service->model
prefetch_related to avoid N+1 queries
SerializerMethodField to expose computed metadata like item count without modifying the database schema
4.service layer
implemented order creation via a service layer that converts cart items into order items while maintaining price snapshots and clearing the cart.
5.view
optimized nested serialization using 
6.validations
7.testing
extra feauture: control nested depth
dont send unecessary data like stock and timestamps
 
Day 10: 3/4/26 ( system design)
 Order transactions (atomic)
 1.Database transactions
 # 🟢 Order Transactions (Atomic) — Summary

## 🔹 1. Database Transactions
- Used `transaction.atomic()` to wrap entire order creation
- Ensures all operations succeed or rollback on failure

**Concepts:** Atomicity (ACID), Consistency, Rollback


## 🔹 2. Row-Level Locking
- Used `select_for_update()` on product variants
- Optimized by locking all variants in a single query (avoided N+1)

**Concepts:** Pessimistic locking, Concurrency control, Race condition prevention


## 🔹 3. Stock Validation
- Validated stock inside transaction (`if stock < quantity`)
- Raised error if insufficient

**Concepts:** Data integrity, Defensive programming


## 🔹 4. Stock Reduction
- Reduced stock inside transaction
- Used `update_fields=["stock"]` for optimized updates

**Concepts:** Controlled state mutation, Efficient DB writes


## 🔹 5. Bulk Operations
- Used `bulk_create()` for creating order items

**Concepts:** Batch processing, Reduced DB queries, Scalability


## 🔹 6. Failure Handling
- Handled:
  - Validation errors → 400
  - Database errors → 500
  - Unexpected errors → 500
- Added logging (`warning`, `error`, `critical`)

**Concepts:** Graceful error handling, Observability, Secure responses


## 🔹 7. Cart Consistency
- Cleared cart only after successful transaction
- Used `select_for_update()` before delete

**Concepts:** Cross-entity consistency, Race condition safety


## 🔹 8. Query Optimization
- Used `select_related()` and `prefetch_related()`
- Eliminated N+1 queries

**Concepts:** ORM optimization, Efficient data fetching


## 🔹 9. API Design
- Standardized response format:
  ```json
  { "success": true/false, "data/message": ... }
 2.Inventory 
 -create inventory model
    seperatio of concerns
    reserved stock
    safety stock
    available_stock()
    indexing
    onetoone relationshop
-register in admin , make migrations
3.stock migration
backup db: copy db.sqlite3 db_backup.sqlite3

 3.Stock validation
 4.Stock reduction
 6.Idempotency
 7.Order status flow
 8.Security
 9.Performance
 10.Add order history , detail api and pagination
    transaction.atomic() — no partial writes
    select_for_update() — prevents race conditions
    Two-phase validation — avoids inconsistent state
    bulk_create — efficient
    Decimal — correct for money
    Logging + error handling — good

“I aggregate requested quantities per product variant before validation to prevent overselling in edge cases.
“I optimized inventory updates using bulk_update to reduce database writes and improve performance under load.”

 Inventory system

 Inventory locking (select_for_update)
 Payment simulation
 MUST DO:
 1. Idempotency
 problem:
 User clicks "Place Order" twice
→ 2 requests hit backend
→ 2 orders created ❌
✅ Solution
Attach a unique key to request
→ Backend checks if already processed
→ If yes → return existing order
→ If no → create new order



2. Order status flow
3. RBAC
4. Order APIs (pagination, history)
IF POSSIBLE
5. Payment simulation
6. Redis caching
7. Rate limiting
bonus:
8. Docker + Deployment
- Recommendation system
- Analytics dashboard
 
 Day 12
⚡ Enhancements (after core works)
 Reviews & ratings
 RBAC (Admin / Seller / Customer)
 Address system

Day 13
 Phase 3: Advanced Backend engineering
✅ Redis caching
✅ Celery background jobs - async tasks
✅ Email system
✅ Payment simulation logic
✅ Rate limiting
✅ API throttling


PHASE 4 — Intelligence Layer (Week 9–10)
Recommendation system
Analytics tracking
Popular products ranking
Sales dashboard API

PHASE 5 — Production Engineering (Week 11–12)
Dockerize project
Setup Nginx
Gunicorn
Environment configs
Logging
Write test cases
Add GitHub Actions CI/CD
Deploy (Render / AWS / DigitalOcean) AWS S3 EC2

Front end: React

Resume descrition:
Built a scalable E-commerce backend using Django and Django REST Framework with features including JWT authentication, product catalog, cart, and order management.Implemented atomic order transactions, optimized database queries, and designed RESTful APIs following best practices.
Integrated caching (Redis) and async processing (Celery) to enhance performance and scalability.inventory locking using database transactions, Dockerized deployment, and CI/CD integration.

Built a scalable AI-enhanced e-commerce backend using Django REST Framework with JWT authentication, Redis caching, Celery async processing, inventory locking using database transactions, Dockerized deployment, and CI/CD integration.