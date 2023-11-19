import random

from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView

from api.models import Recipe, Ingredient, UserFeedback
from api.serializers import UserSerializer, GroupSerializer, RecipeSerializer, IngredientSerializer
from api.recommender import get_next_recommendation


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]


class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]


def recommend(request, id, exclude_ids):
    """
    Recommend a recipe based on the recipe with the given id

    :param request: HTTP request
    :param id: id of the recipe to base the recommendation on
    :return: HTTP response
    """

    # We have to start with some recommendation.
    # For testing, we use id=1
    # We then start the recommendation based on the recipe with id 1
    # We recommend similar recipes to the recipe with id 1
    # Based on the user feedback in the database we adjust the recommendations by adjusting the similarity between recipes

    # Example requests:
    # http://127.0.0.1:8000/api/recommend/2/-1/
    # Initially call this as default. It will exclude the recipe with id -1 from the recommendations which does not exist

    # Afterwards, append every recipe id that the user has seen and liked to the exclude_ids list
    # E.g. http://127.0.0.1:8000/api/recommend/2/1,5,3/
    # if the user has seen recipes with id 1, 5 and 3

    exclude_ids = exclude_ids.split(',')
    exclude_ids = [int(id) for id in exclude_ids]

    elem = Recipe.objects.filter(id=id)
    if len(elem) == 0:
        # TODO: Alternatively return random recipe in the error case
        return HttpResponse(f"Recipe with id {id} does not exist. Excluded ids from search: {', '.join([str(id) for id in exclude_ids])}")

    recommendation = get_next_recommendation(id, exclude_ids=exclude_ids)
    return HttpResponse(f"{recommendation}")


def reduce_list_size(input_list, target_size):
    if target_size >= len(input_list):
        return input_list  # No need to reduce the size

    random_elements = random.sample(input_list, target_size)
    return random_elements

def recommendation(request):
    user = request.user
    user_feedback = UserFeedback.objects.filter(user=user)
    user_feedback_negative = UserFeedback.objects.filter(user=user, feedback=-1)
    user_feedback_positive = UserFeedback.objects.filter(user=user, feedback=1)

    # All recipes that the user has swiped are excluded
    exclude_ids = list(user_feedback.values_list('recipe_id', flat=True))

    # This list contains all recommended recipes
    recommendation = []

    # Cumpute set of recipes that have no feedback from user
    all_ids = list(Recipe.objects.all().values_list('id', flat=True))
    compset = list(set(all_ids) - set(exclude_ids))

    # Reduce size to 5 elements
    compset = reduce_list_size(compset, 5)

    # Recommend a item for each of this items
    for recipe_id_without_feedback in compset:
         recommended = get_next_recommendation(recipe_id_without_feedback, exclude_ids=exclude_ids)
         recommendation.append(recommended)

    return HttpResponse(f"{recommendation}")


class CustomAutoSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        return


class LikeView(APIView):
    def post(self, request, recipeId):
        feedback = UserFeedback(feedback=1, recipe_id=recipeId, user=request.user)
        feedback.save()
        # Implement logic to handle liking
        return Response({'message': 'Liked successfully!'}, status=status.HTTP_200_OK)


class DislikeView(APIView):
    def post(self, request, recipeId):
        feedback = UserFeedback(feedback=-1, recipe_id=recipeId, user=request.user)
        feedback.save()
        # Implement logic to handle disliking
        return Response({'message': 'Disliked successfully!'}, status=status.HTTP_200_OK)
