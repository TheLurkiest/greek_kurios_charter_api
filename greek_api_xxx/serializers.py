from rest_framework import serializers
from .models import Songs

# this file I had to create-- along with the urls
# file within greek_api_xxx-- the other files that
# I needed to write to directly to get this started
# was just a matter of editing files that already
# been created automatically/indirectly by the two
# starting django-admin commands I used to start.

class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ("title", "artist")
