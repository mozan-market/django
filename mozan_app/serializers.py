from django.forms import widgets
from rest_framework import serializers
from mozan_app.models import Post, UserProfile, Category, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'original_image')

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    # Need to solve categories issue. The way they are represented and viewed.
    # category = serializers.ChoiceField(source='category.name', )

    class Meta:
        model = Post
        fields = ('id', 'content', 'owner', 'category', 'images')

    def create(self, validated_attrs):
        return Post.objects.create(**validated_attrs)

    def update(self, instance, validated_attrs):
        instance.content = validated_attrs.get('content', instance.content)
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedIdentityField('posts', view_name='userpost-list',
                                                 lookup_field='username')

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'posts',)
