from django.forms import widgets
from rest_framework import serializers
from karma_app.models import Post, User, Category

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('id', 'content', 'user', 'category',) 

    def create(self, validated_attrs):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Post.objects.create(**validated_attrs)

    def update(self, instance, validated_attrs):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.content= validated_attrs.get('content', instance.content)
        instance.save()
        return instance

