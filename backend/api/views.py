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



class CustomAutoSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        return


class LikeView(APIView):
    def get(self, request, pk):
        feedback = UserFeedback(feedback=1, recipe_id=pk, user=request.user)
        feedback.save()
        # Implement logic to handle liking
        return Response({'message': 'Liked successfully!'}, status=status.HTTP_200_OK)


class DislikeView(APIView):
    def get(self, request, pk):
        feedback = UserFeedback(feedback=-1, recipe_id=pk, user=request.user)
        feedback.save()
        # Implement logic to handle disliking
        return Response({'message': 'Disliked successfully!'}, status=status.HTTP_200_OK)
