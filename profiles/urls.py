from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles import views

routers = DefaultRouter()
routers.register('profile', views.UserProfileViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('login/', views.UserLoginApiView.as_view()),
]
