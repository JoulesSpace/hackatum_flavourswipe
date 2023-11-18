from django.contrib import admin
from .models import Ingredient, UserFeedback
from .models import Recipe 

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(UserFeedback)

