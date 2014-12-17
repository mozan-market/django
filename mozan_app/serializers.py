from rest_framework import serializers
from mozan_app.models import Post, UserProfile, Category, Image, User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile')

    def create(self, validated_attrs):
        return User.objects.create(**validated_attrs)

    def update(self, instance, validated_attrs):
        instance.content = validated_attrs.get('content', instance.content)
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'avatar_original_image')

    def create(self, validated_attrs):
        return UserProfile.objects.create(**validated_attrs)

    def update(self, instance, validated_attrs):
        instance.content = validated_attrs.get('content', instance.content)
        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('post', 'id', 'original_image')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name',)


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    #user = serializers.PrimaryKeyRelatedField()
    # Need to solve categories issue. The way they are represented and viewed.
    category = CategorySerializer()
    images = ImageSerializer()

    class Meta:
        model = Post
        fields = ('id', 'content', 'owner', 'category', 'images', )

    def create(self, validated_attrs):
        return Post.objects.create(**validated_attrs)

    def update(self, instance, validated_attrs):
        instance.content = validated_attrs.get('content', instance.content)
        instance.save()
        return instance