# greek_kurios_charter_api

-----------------------------------------------------------------------
Terminal Commands That’ll be Used Frequently:
to start this server up again, at some later date, this single command is needed-- the one command needed now, to do this all again is:
python manage.py runserver

...and it sounds like you need to do these 2 commands after making major changes:
python manage.py makemigrations
python manage.py migrate
...and to test things out we use: python manage.py test
...and URL’s of interest we can use to test if it’s working are:
http://127.0.0.1:8000/admin/
http://127.0.0.1:8000/admin/music/songs/


-----------------------------------------------------------------------
-----------------------------------------------------------------------
-----------------------------------------------------------------------

NOTE- one more addition:
...don't forget to alter api/settings.py using atom
...to include (within INSTALLED_APPS):
'rest_framework',
'greek_api_xxx',

NOTE- one more addition #2:
...after all these steps are completed-- use the migrate commands to create
model songs... then do this:
python manage.py createsuperuser --email admin@example.com --username admin
...to create a place where this info will be stored-- I'm going to use my
unh username and password for THIS one.


To create a new API based on this one it’s as simple as A, B, C:

Blue text is created through:

A) django-admin startproject api .
  ...which creates: config, manage.py, and README.md
  ...and the 4 files within api:  init, settings, urls, and wsgi…

Red text is created through running the following:
B) django-admin startapp peanut_farmer_api_xxx
  ...and pink text I’m unsure of but THINK is created through this too

 1) music/models.py
 2) music/admin.py
 3) music/serializers.py
 4) music/views.py
 5) api/urls.py
 6) music/urls.py
 7) music/tests.py

Where edits are as follows:

from django.test import TestCase
C) The following (gold text) need to be edited in directly:

-----------------------------------------------------------------------
Steps 1-7:
1 Edit music/models.py
2 Edit music/admin.py
    occasionally Migrate and makemigrate... but frequently give us errors while construction in progress
3 Edit music/serializers.py
4 Edit music/views.py
5 Edit api/urls.py
6 Edit music/urls.py
7 Edit music/tests.py
-----------------------------------------------------------------------

The final completed python files produced by steps 5a-5g look something like this:
--------------------
1)
from django.db import models

# Create your models here.

class Songs(models.Model):
    # song title
    title = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    artist = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)
--------------------
2)
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Songs

admin.site.register(Songs)
--------------------
3)
from rest_framework import serializers
from .models import Songs


class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ("title", "artist")
--------------------
4)
from rest_framework import generics
from .models import Songs
from .serializers import SongsSerializer


class ListSongsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
--------------------
5)
"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('api/(?P<version>(v1|v2))/', include('music.urls'))
]
--------------------
6)

from django.urls import path
from .views import ListSongsView


urlpatterns = [
    path('songs/', ListSongsView.as_view(), name="songs-all")
]

--------------------
7)

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_song(title="", artist=""):
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)

    def setUp(self):
        # add test data
        self.create_song("like glue", "sean paul")
        self.create_song("simple song", "konshens")
        self.create_song("love is wicked", "brick and lace")
        self.create_song("jam rock", "damien marley")


class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("songs-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

-----------------------------------------------------------------------
