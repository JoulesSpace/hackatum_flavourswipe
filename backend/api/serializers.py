from django.conf import settings
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.models import Recipe, Ingredient


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['url', 'name']


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return settings.STATIC_URL + obj.image_id

    class Meta:
        model = Recipe
        fields = ['url', 'name', 'description', 'difficulty', 'duration', 'ingredients', 'image_id', 'image_url']

