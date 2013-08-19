import json

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status

from ftchr.models import ProfileModel

from scripts.fetcher import facebook, twitter

_facebook, _twitter = settings.NETWORKS.split("|")
getter = {_facebook: facebook, _twitter: twitter}

class Profile(APIView):

    renderer_classes = [JSONRenderer,]
    parser_classes = [JSONParser,]
    
    def get(self, request, network, username):
        try:
            profile = ProfileModel.objects.get(
                network=network, username=username)
            count=profile.count
            description=profile.description
        except ObjectDoesNotExist:
            data = getter[network](username)
            count = data['count'] or 0
            description = data['description'] or ''
            ProfileModel(network=network, username=username,
                         count=count, description=description).save()
        if not (count and description):
            return Response(dict(WARNING="No data available"))
        else:
            return Response(dict(count=count, description=description))


    def delete(self, request, network, username):
        try:
            ProfileModel.objects.get(network=network, username=username)
            ProfileModel.objects.filter(
                network=network, username=username).delete()
            return Response(dict(INFO="Deleted"))
        except ObjectDoesNotExist:
            return Response(dict(ERROR="Not Found"), status=status.HTTP_404_NOT_FOUND)

    def put(self, request, network, username):
        try:
            profile = ProfileModel.objects.get(
                network=network, username=username)
        except ObjectDoesNotExist:
            return Response(dict(ERROR="Not Found"), status=status.HTTP_404_NOT_FOUND)
        data = json.loads(request.stream.read())
        to_save = False
        if "count" in data:
            profile.count = data['count']
            to_save = True
        if "description" in data:
            profile.description = data['description']
            to_save = True
        if to_save:
            profile.save()
            return Response(dict(INFO="Updated"))
        else:
            return Response(dict(WARNING="Nothing updated"))
            
class ProfileMaker(APIView):

    renderer_classes = [JSONRenderer,]
    parser_classes = [JSONParser,]


    def post(self, request, network):
        # just json request
        data = json.loads(request.stream.read())
        if "user" in data:
            if len(ProfileModel.objects.filter(username=data['user'],
                                               network=network)) > 0:
                return Response(dict(ERROR="Username already exist"),
                                     status=status.HTTP_409_CONFLICT)
            profile = ProfileModel(
                username=data['user'],
                network=network,
                count=data.get('count', 0),
                description=data.get('description', ''))
            profile.save()
            return Response(dict(INFO="Created"), status=status.HTTP_201_CREATED)
        else:
            return Response(dict(ERROR="No user provided"), status=status.HTTP_400_BAD_REQUEST)
