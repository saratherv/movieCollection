from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from core.serializers import *
import requests, json
from core.otherRequests import fetchMovies

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status_code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class MoviesAPIView(ListAPIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        page = request.GET.get("page", 1)
        try:
            data = fetchMovies(page)
            return Response(data, status=status.HTTP_200_OK)
        except :        
            return Response({"success" : False, "error" : "maximum retries exceeded"}, status=status.HTTP_400_BAD_REQUEST)
        


class CollectionListView(CreateAPIView, ListAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        collections = Collection.objects.filter(user=request.user)
        serializer = CollectionSerializer(collections, many=True)
        favourite_genres = Movies.objects.filter(collection__user=request.user).order_by("-created")[:3].values_list("genres", flat=True)
        return Response({"sucess" : True,'status_code' : status.HTTP_200_OK, "data" : { "collections" : serializer.data, "favourite_genres" : list(favourite_genres) }})

    def post(self, request):
        serializer = MovieCollectionSerializer(data=request.data, context={"user" : request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"succes" : True, 'status_code' : status.HTTP_200_OK, "uuid" : serializer.data["uuid"]})


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
        return Response({"success" : True, 'status_code' : status.HTTP_200_OK, "data" : serializer.data})
    
    def put(self, request, pk):
        collection = self.get_object(pk)
        if not collection:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success" : True, 'status_code' : status.HTTP_200_OK, "data" : serializer.data})
        return Response({"success" : False, "status_code" : status.HTTP_400_BAD_REQUEST, "error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        collection = self.get_object(pk)
        if not collection:
            return Response(status=status.HTTP_404_NOT_FOUND)
        collection.delete()
        return Response({"success" : True, 'status_code' : status.HTTP_200_OK, "message" : "collection deleted successfully"})



class RequestCounterView(CreateAPIView, RetrieveAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request_count = RequestCounter.objects.all().first()
        if request_count:
            return Response({"success" : True, 'status_code' : status.HTTP_200_OK, "requests" : request_count.requests})
        else:
            return Response({ "requests" : 0})
    
    def post(self, request):
        request_count = RequestCounter.objects.all().first()
        if request_count:
            request_count.requests = 0
            request_count.save()
        return Response({"success" : True, 'status_code' : status.HTTP_200_OK, "message" : "request count reset successfully"})
        


