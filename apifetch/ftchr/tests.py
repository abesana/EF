import json

from django.test import TestCase
from django.test.client import Client
from rest_framework import status

from ftchr.models import ProfileModel



class ProfileTestCase(TestCase):

    def setUp(self):
        ProfileModel.objects.create(username="foo", network="twitter", count=23, description="foo description")

    def tearDown(self):
        ProfileModel.objects.all().delete()


    def test_profile_get(self):
        c = Client()
        response = c.get('/network/twitter/username/foo')
        self.assertEqual({u'count': 23, u'description': u'foo description'},
                         json.loads(response.content))

    def test_profile_delete(self):
        c = Client()
        c.delete('/network/twitter/username/foo')
        self.assertEqual(0, len(list(ProfileModel.objects.all())))

    def test_profile_put(self):
        c = Client()
        response = c.put('/network/twitter/username/foo', json.dumps(
            {'count': 89, "description": "foo description changed"}),
                          content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_profile_post_conflict(self):
        c = Client()
        response = c.post('/network/twitter/username', json.dumps(
            {'count': 23, "user": "foo", "description": "foo description"}),
                          content_type="application/json")
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
       
    def test_profile_post(self):
        c = Client()
        response = c.post('/network/twitter/username', json.dumps(
            {'count': 23, "user": "bar", "description": "foo description"}),
                          content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
