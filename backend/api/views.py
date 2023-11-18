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


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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
