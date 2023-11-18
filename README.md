# Hackatum FlavourSwipe

**Tech Stack**

|  | Tech                  |
| --- |-----------------------|
| Frontend | Flutter               |
| Backend | Python, Django, SQLite |

## Frontend

## Backend

To get started, we need a working Python environment.
We need to move to the 'backend' directory and install all dependencies:
```
pip install -r requirements.txt
```

Now, run our database migrations.
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
