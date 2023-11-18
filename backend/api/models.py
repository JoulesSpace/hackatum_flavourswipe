from django.conf import settings
from django.db import models


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    difficulty = models.IntegerField()
    duration = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient)
    image_id = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class UserFeedback(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    feedback = models.IntegerField()
