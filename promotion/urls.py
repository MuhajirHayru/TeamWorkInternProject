from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreatePostView, ApprovePostView, PostViewSet
from . import views

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
from promotion.views import EventCreating

urlpatterns = [
    path('api/create-post/', CreatePostView.as_view(), name='create-post'),
    path('api/posts/<int:pk>/approve/', ApprovePostView.as_view(), name='approve-post'),
    path('', include(router.urls)),
    path("api/create/",views.createGenerics.as_view()),
    path("api/job",views.jobCreations.as_view()),
    path("jposts",views.listingjobs.as_view()),
    path("api/v1/EventCreation/",views.EventCreating.as_view()),
]
