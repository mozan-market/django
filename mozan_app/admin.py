from django.contrib import admin
from mozan_app.models import UserProfile, Post, Image, Category
from mptt.admin import MPTTModelAdmin

# Register your models here.

class ImageInline(admin.TabularInline):
    model = Image

class PostAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]



admin.site.register(UserProfile)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, MPTTModelAdmin)
 
