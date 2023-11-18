from django.urls import include, path
from rest_framework import routers
from api import views
from .views import LikeView, DislikeView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'recipe', views.RecipeViewSet)
router.register(r'ingredient', views.IngredientViewSet)

from . import views

urlpatterns = [
    path("recommend/<int:id>/<str:exclude_ids>/", views.recommend, name="recommend"),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('like/<int:pk>/', LikeView.as_view(), name='like'),
    path('dislike/<int:pk>/', DislikeView.as_view(), name='dislike'),
]