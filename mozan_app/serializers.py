from django.forms import widgets
from rest_framework import serializers
from mozan_app.models import Post, UserProfile, Category, Image

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('id', 'content', 'user', 'category',) 

    def create(self, validated_attrs):
        """
        Create and return a new `Post` instance, given the validated data.
        """
        return Post.objects.create(**validated_attrs)

    def update(self, instance, validated_attrs):
        """
        Update and return an existing `Post` instance, given the validated data.
        """
        instance.content= validated_attrs.get('content', instance.content)
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
   
  
    class Meta:
        model = UserProfile
        fields = ('id', 'user',  )
                                
