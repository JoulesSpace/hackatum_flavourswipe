from django.contrib import admin
from .models import Ingredient
from .models import Recipe 


class RecipeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "difficulty", "duration", "image_id"]


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)

