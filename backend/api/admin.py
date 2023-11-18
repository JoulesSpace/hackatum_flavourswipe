from django.contrib import admin
from .models import Ingredient, UserFeedback
from .models import Recipe 


class RecipeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "difficulty", "duration", "image_id"]


class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ["user", "recipe", "feedback"]


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(UserFeedback, UserFeedbackAdmin)


