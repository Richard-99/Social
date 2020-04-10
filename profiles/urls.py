from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles import views

routers = DefaultRouter()
routers.register('profile', views.UserProfileViewSet, basename="profile")
routers.register('feed', views.UserProfileFeedViewSet, basename="feed")
routers.register('message', views.MessagingViewSet, basename="message")

urlpatterns = [
    path('', include((routers.urls, 'profiles'), namespace='api')),
    path('login/', views.UserLoginApiView.as_view()),
]
