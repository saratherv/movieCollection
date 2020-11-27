import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    
    def create_user(self, username, password=None):
        """
        Create and return a `User` with an username and password.
        """
        if not username:
            raise ValueError('Users Must Have an username')

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(
        max_length=255,
        unique=True
        )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "login"


class Collection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title) + " : " + str(self.user)


class Movies(models.Model):
    uuid = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    genres = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, related_name="movies", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title) + " : " + str(self.collection)


class RequestCounter(models.Model):
    requests = models.PositiveIntegerField()
    
    def __str__(self):
        return str(self.requestCount)
