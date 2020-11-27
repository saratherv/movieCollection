from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from core.serializers import *
import requests, json
from movieCollection.settings.base import credy_password, credy_username


class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class MoviesAPIView(ListAPIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        page = request.GET.get("page", 1)
        url = f"https://demo.credy.in/api/v1/maya/movies/?page={page}"
        response = requests.get(url=url, auth=(credy_username, credy_password))
        if response.status_code == 200:
            data = json.loads(response.content)
            return Response(data, status=status.HTTP_200_OK)
        


class CollectionListView(CreateAPIView, ListAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        collections = Collection.objects.filter(user=request.user)
        serializer = CollectionSerializer(collections, many=True)
        favourite_genres = Movies.objects.filter(collection__user=request.user).order_by("-created")[:3].values_list("genres", flat=True)
        return Response({"is_sucess" : True, "data" : { "collections" : serializer.data, "favourite_genres" : favourite_genres }})

    def post(self, request):
        serializer = MovieCollectionSerializer(data=request.data, context={"user" : request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"succes" : True, "uuid" : serializer.data["uuid"]})


class CollectionView(UpdateAPIView, RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = MovieCollectionSerializer

    def get_object(self, pk):
        try:
            collection = Collection.objects.get(uuid=pk)
            return collection
        except Collection.DoesNotExist:
            return None
    
    def get(self, request, pk):
        collection = self.get_object(pk)
        if not collection:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(collection)
        return Response(serializer.data)
    
    def put(self, request, pk):
        collection = self.get_object(pk)
        if not collection:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        collection = self.get_object(pk)
        if not collection:
            return Response(status=status.HTTP_404_NOT_FOUND)
        collection.delete()
        return Response({"success" : True, "message" : "collection deleted successfully"})
