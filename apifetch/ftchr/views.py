
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from ftchr.models import ProfileModel

from fetcher import facebook, twitter

_facebook, _twitter = settings.NETWORKS.split("|")
getter = {_facebook: facebook, _twitter: twitter}

class Profile(APIView):
    """
    
    """
    renderer_classes = [JSONRenderer,]
    
    def get(self, request, network, username):
        try:
            profile = ProfileModel.objects.get(network=network, username=username)
            count=profile.count
            description=profile.description
        except ObjectDoesNotExist:
            data = getter[network](username)
            count = data['count'] or 0
            description = data['description'] or ''
            ProfileModel(network=network, username=username,
                         count=count, description=description).save()
        return Response(dict(count=count, description=description))
