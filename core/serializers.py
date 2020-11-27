from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from core.models import *



JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            user = User.objects.create_user(**data)
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exists'
            )
        return {
            'username':user.username,
            'token': jwt_token
        }


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ("uuid","title","description",)


class MoviesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movies
        fields = ("uuid","title","description","genres",)
    

class MovieCollectionSerializer(serializers.ModelSerializer):

    movies = MoviesSerializer(many=True)

    class Meta:
        model = Collection
        fields = ("uuid","title","description", "movies",)
    
    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        collection = Collection.objects.create(**validated_data, user=self.context.get("user"))
        for data in movies_data:
            Movies.objects.create(
                uuid = data["uuid"],
                title = data["title"],
                description = data["description"],
                genres = data["genres"],
                collection = collection
            )
        return collection
    
    def update(self,instance, validated_data):
        movies_data = validated_data.pop('movies')
        collection = super().update(instance, validated_data)
        for data in movies_data:
            Movies.objects.update_or_create(
                uuid=data["uuid"],
                collection = collection,
                defaults={
                "uuid" : data["uuid"],
                "title" : data["title"],
                "description" : data["description"],
                "genres" : data["genres"]
                }
            )
        return collection
