"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TeamViewSet, ActivityViewSet, LeaderboardViewSet, WorkoutViewSet, api_root
from django.conf import settings
from rest_framework.settings import api_settings
from rest_framework.renderers import BrowsableAPIRenderer
import os



# Patch BrowsableAPIRenderer to use codespace URL if available for API docs
class PatchedBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_default_renderer_context(self):
        context = super().get_default_renderer_context()
        codespace_name = os.environ.get('CODESPACE_NAME')
        if codespace_name:
            # Set the host and scheme for the API docs UI
            context['request'].META['HTTP_HOST'] = f"{codespace_name}-8000.app.github.dev"
            context['request'].scheme = 'https'
        return context

if BrowsableAPIRenderer in api_settings.DEFAULT_RENDERER_CLASSES:
    idx = api_settings.DEFAULT_RENDERER_CLASSES.index(BrowsableAPIRenderer)
    api_settings.DEFAULT_RENDERER_CLASSES = list(api_settings.DEFAULT_RENDERER_CLASSES)
    api_settings.DEFAULT_RENDERER_CLASSES[idx] = PatchedBrowsableAPIRenderer

# Setup router for REST API endpoints
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', api_root, name='api-root'),
]
