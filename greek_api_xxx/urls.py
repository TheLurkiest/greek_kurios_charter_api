from django.urls import path
from .views import ListSongsView

# this file I had to create-- along with serializers.py
# were the only files of those that I needed to write to
# directly to get started-- that required that I actually
# CREATE the file-- rather than just editing one that was
# created automatically by the 2 django-admin commands

urlpatterns = [
    path('songs/', ListSongsView.as_view(), name="songs-all")
]
