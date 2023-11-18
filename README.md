# Hackatum FlavourSwipe

## Frontend

## Backend

At first, we have to move to the 'backend' and run our database migrations.
```
python manage.py migrate
```

Next, we can create a user for the backend:
```
python manage.py createsuperuser --email mickymouse@disney.com --username admin
```

Finally let's run the server:
```
python manage.py runserver
```

**URLs:**
- http://127.0.0.1:8000/admin/
- http://127.0.0.1:8000/api/
