from django.test import TestCase, Client
from rest_framework.test import APIClient
from core.models import *
from django.contrib.auth.models import User
import json
from rest_framework import status
from django.urls import reverse
from core.serializers import *
# Create your tests here.


class CollectionListTestCase(TestCase):

    def get_user(self, username, password):
        client = APIClient()
        response = self.client.post(reverse('register'), data={"username" : username,"password" : password})
        return response.data['token']

    def setUp(self):
        self.token = self.get_user("test_user@test.com",  "TestPassword")
        self.user = User.objects.get(username="test_user@test.com")
        self.token1 = self.get_user("test_user1@test.com",  "TestPassword1")
        self.user1 = User.objects.get(username="test_user1@test.com")
        self.collection1 = Collection.objects.create(title="test_title", description="test_description", user=self.user)
        self.Movie1 = Movies.objects.create(title="test_movie_title1", description="test_movie_description1",
                            genres="test_genres1", uuid="test1-1526-4103-9ba6-34c24c1d640d", collection=self.collection1)
        self.Movie2 = Movies.objects.create(title="test_movie_title2", description="test_movie_description2",
                            genres="test_genres2", uuid="test2-1526-4103-9ba6-34c24c1d640d", collection=self.collection1)
        self.data1 = {
                "title" : "My test Title",
                "description" : "I like this collection",
                "movies" : [
                    {
                        "title": "Les affiches en goguette",
                        "description": "A wall full of advertising posters comes to life.",
                        "genres": "Fantasy,Comedy",
                        "uuid": "9bd8a0cf-1526-4103-9ba6-34c24c1d640d"
                    },
                    {
                        "title": "Les cartes vivantes",
                        "description": "A bearded magician holds up a large playing card and makes it larger. He tears up a card of a queen, burns the torn bits, and a life-size Queen of Hearts card appears; then, it becomes alive. The magician puts her back into the card. The same thing happens with the King of Clubs: the card becomes alive. The king removes his costume, and there's something very familiar about him. (IMDb)",
                        "genres": "Fantasy",
                        "uuid": "a43bfbdd-e1c3-4d88-ba7a-a2faa05e32fe"
                    }
                ]
            }
        self.data2 = {
                "description" : "I like this collection",
                "movies" : [
                    {
                        "title": "Les affiches en goguette",
                        "description": "A wall full of advertising posters comes to life.",
                        "genres": "Fantasy,Comedy",
                        "uuid": "9bd8a0cf-1526-4103-9ba6-34c24c1d640d"
                    },
                    {
                        "title": "Les cartes vivantes",
                        "description": "A bearded magician holds up a large playing card and makes it larger. He tears up a card of a queen, burns the torn bits, and a life-size Queen of Hearts card appears; then, it becomes alive. The magician puts her back into the card. The same thing happens with the King of Clubs: the card becomes alive. The king removes his costume, and there's something very familiar about him. (IMDb)",
                        "genres": "Fantasy",
                        "uuid": "a43bfbdd-e1c3-4d88-ba7a-a2faa05e32fe"
                    }
                ]
            }

    def test_get_collection(self):
        client = APIClient()

        ##### testing base case ######
        response = self.client.get(reverse("collectionList"), content_type = "application/json", HTTP_AUTHORIZATION = 'Bearer ' + self.token)
        collections = Collection.objects.filter(user=self.user)
        serializer = CollectionSerializer(collections, many=True)
        favourite_genres = Movies.objects.filter(collection__user=self.user).order_by("-created")[:3].values_list("genres", flat=True)
        self.assertEqual(response.data["data"]["collections"], serializer.data)
        self.assertEqual(response.data["data"]["favourite_genres"], list(favourite_genres))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #### testing case when there are no collections ####
        response = self.client.get(reverse("collectionList"), content_type = "application/json", HTTP_AUTHORIZATION = 'Bearer ' + self.token1)
        collections = Collection.objects.filter(user=self.user1)
        serializer = CollectionSerializer(collections, many=True)
        favourite_genres = Movies.objects.filter(collection__user=self.user1).order_by("-created")[:3].values_list("genres", flat=True)
        self.assertEqual(response.data["data"]["collections"], serializer.data)
        self.assertEqual(response.data["data"]["favourite_genres"], list(favourite_genres))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #### testing case without auth token ####
        response = self.client.get(reverse("collectionList"), content_type = "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_collection(self):
        client = APIClient()

        #### testing base case ####
        
        response = self.client.post(
                            reverse('collectionList'), 
                            data=json.dumps(self.data1), 
                            content_type = "application/json", 
                            HTTP_AUTHORIZATION = 'Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #### check case when required field is missing #####
        response = self.client.post(
                            reverse('collectionList'), 
                            data=json.dumps(self.data2), 
                            content_type = "application/json", 
                            HTTP_AUTHORIZATION = 'Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

