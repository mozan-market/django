from django.db import models
from django.contrib.auth.models import User
import hashlib
from django.core.files.storage import FileSystemStorage
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Karma(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now=True, blank=True)
    image = models.ImageField(upload_to='post_images/', 
                              default = '',)
    image_main_page = ImageSpecField(source='image',
                                      processors=[ResizeToFill(236, 180)],
                                      format='JPEG',
                                      options={'quality': 60})
 

    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
 
    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=30" % hashlib.md5(self.user.email).hexdigest()
 
 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])