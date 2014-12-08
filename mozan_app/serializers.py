from django.forms import widgets
from rest_framework import serializers
from mozan_app.models import Post, UserProfile, Category, Image

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.Field('image.url')
    class Meta:
        model = Image
        
class PostSerializer(serializers.ModelSerializer):
    images = serializers.HyperlinkedIdentityField('images', view_name='postimage-list')
    class Meta:
        model = Post
        fields = ('id', 'content', 'user', 'category', 'images') 
    def create(self, validated_attrs):
        return Post.objects.create(**validated_attrs)
    def update(self, instance, validated_attrs):
        instance.content= validated_attrs.get('content', instance.content)
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedIdentityField('posts', view_name='userpost-list', lookup_field='username')
    class Meta:
        model = UserProfile
        fields = ('id', 'user','posts',  )
                                
