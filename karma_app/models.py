from django.db import models
from django.contrib.auth.models import User
import hashlib
from django.core.files.storage import FileSystemStorage
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Adjust
from mptt.models import MPTTModel, TreeForeignKey



    
class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name 
    
    class MPTTMeta:
        order_insertion_by = ['name']
    

class Post(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    creation_date = models.DateTimeField(auto_now=True, blank=True)
   
    def __unicode__(self):
        return self.content 

class Image(models.Model):
	post = models.ForeignKey(Post)

	original_image = models.ImageField(upload_to='post_images/', 
                              default = '',)
	image_main_page = ImageSpecField(source='original_image', processors=[ResizeToFill(236, 180)], format='JPEG', options={'quality': 60})
	image_post_page = ImageSpecField(source='original_image', processors=[ResizeToFit(480, 480), Adjust(contrast=1.2, sharpness=1.1)], format='JPEG', options={'quality': 75})


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
 
    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=30" % hashlib.md5(self.user.email).hexdigest()
 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])



from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=Image)
def image_post_delete_handler(sender, **kwargs):
    image = kwargs['instance']
    storage, path = image.original_image.storage, image.original_image.path
    storage.delete(path)

