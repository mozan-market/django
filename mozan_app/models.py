from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Adjust
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Post(models.Model):
    content = models.CharField(max_length=140)
    owner = models.ForeignKey(User, default='', related_name='posts')
    category = models.ForeignKey(Category)
    creation_date = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.content


class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images')
    original_image = models.ImageField(upload_to='post_images', default='', )
    image_main_page = ImageSpecField(source='original_image',
                                     processors=[ResizeToFill(236, 180),
                                                 Adjust(contrast=1.2, sharpness=1.1)],
                                     format='JPEG', options={'quality': 60})
    image_post_page = ImageSpecField(source='original_image',
                                     processors=[ResizeToFit(480, 480)], format='JPEG',
                                     options={'quality': 75})


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    avatar_original_image = models.ImageField(upload_to='avatars/',
                                              default='default/member-photo.png')
    avatar_30 = ImageSpecField(source='avatar_original_image',
                               processors=[ResizeToFill(30, 30),
                                           Adjust(contrast=1.2, sharpness=1.1)],
                               format='JPEG',
                               options={'quality': 80})

    def __unicode__(self):
        return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


@receiver(post_delete, sender=Image)
def image_post_delete_handler(sender, **kwargs):
    image = kwargs['instance']
    storage, path = image.original_image.storage, image.original_image.path
    storage.delete(path)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
