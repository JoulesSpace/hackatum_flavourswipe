from django.contrib import admin
from .models import Ingredient
from .models import Recipe 

admin.site.register(Ingredient)
admin.site.register(Recipe)

