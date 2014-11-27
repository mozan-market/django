from django.contrib import admin
from karma_app.models import Post, Category
from mptt.admin import MPTTModelAdmin

# Register your models here.




admin.site.register(Post)
admin.site.register(Category, MPTTModelAdmin)
 