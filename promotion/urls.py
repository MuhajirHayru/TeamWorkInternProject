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
    #below this i coded from scrach the apis endpoints 

    #for the brand creation and reading or fetching
    path("api/v1/BrandCreation/",views.brandCreating.as_view()),
    path("api/v1/Brands-posted/",views.brandsposted.as_view()),
    # for the service fetching and reading i mean posting and retriving
    path("api/v1/ServiceCreation/",views.servicesCreating.as_view()),
    path("api/v1/Services-posted/",views.EventCreating.as_view()),
    #below this the api for the job announcement
    path("api/v1/JobCreation/",views.JobCreating.as_view()),
    path("api/v1/Jobs-posted/",views.Jobsposted.as_view()),
    #below this the apis for the product
    path("api/v1/ProductCreation/",views.productCreating.as_view()),
    path("api/v1/Products-posted/",views.productPosted.as_view()),
    #api for the comptions details
    path("api/v1/CompetionCreation/",views.CompetionCreating.as_view()),
    path("api/v1/competions-posted/",views.competionsPosted.as_view()),
    #for the event creation and reading
    path("api/v1/EventCreation/",views.EventCreating.as_view()),
    path('api/v1/Eventsposted/',views.Eventsposted.as_view()),
]
