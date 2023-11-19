# Hackatum FlavourSwipe

## Project Overview
This repository contains the source code for a collaborative project 
developed during the HackaTum Hackathon 2023. The goal of our project is 
to create an engaging app, to provide a unique recipe-swiping experience, 
similar to dating apps like Tinder. Our app incorporates sophisticated 
recommendation algorithms to deliver personalized recipe suggestions.

## Features
- Recipe Swiping: Users can swipe through a curated selection of recipes, similar to dating apps.
- Personalized Recommendations: Our recommendation algorithms analyze user preferences to offer personalized recipe suggestions.

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


## API

### Get a list of all recipes
```
GET http://localhost:8000/api/recipe/
```

### Get a list of all ingredients
```
GET http://localhost:8000/api/ingredient/
```

### Submit a like for a receipt
```
POST http://localhost:8000/api/like/<receiptId>/
```

### Submit a dislike for a receipt
```
POST http://localhost:8000/api/dislike/<receiptId>/
```

### Get a receipt recommendation
```
POST http://localhost:8000/api/recommend/<receiptId>/<exclueReceiptIds>/
```
The first time, the receiptId needs to be random, but after that we pass
the current receiptId. For excludeReceiptId we pass all Ids of Receipts
that has been shown previously, separated by comma. As a result we get
a JSON that recommends a similar receipt.

## Scripts

### Generate images using AI for a list of recipes in a csv file
In the directory 'data', we have csv file of recipes and their ingredients.
The following command imports all recipes in the database and creates a image using AI.
```
python manage.py create_data data/Recipes.csv
```


## Acknowledgments
Hello Fresh for providing an exciting challenge for our hackathon.
Contributors to the open-source libraries and frameworks used in this project.
