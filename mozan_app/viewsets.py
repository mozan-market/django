from django.contrib.auth.models import User
from .models import Post, Image
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()


class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()


class ImageViewSet(viewsets.ModelViewSet):
	queryset = Image.objects.all()