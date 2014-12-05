from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from django.contrib import admin

from hitcount.views import update_hit_count_ajax

from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns

admin.autodiscover()

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'karma_app.views.public'), # root
    url(r'^users/(?P<username>\w{0,30})/$', 'karma_app.views.users'),
    url(r'^post/(?P<post_id>\w{0,30})/$', 'karma_app.views.posts'),
    url(r'^follow$', 'karma_app.views.follow'),
    
    url(r'^api/posts/$', 'karma_app.views.post_REST_list'),
    url(r'^api/post/(?P<pk>[0-9]+)/$', 'karma_app.views.post_REST_detail'),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api$', include(router.urls)),

    url(r'^search/', include('haystack.urls')),
    url(r'^counter/ajax/hit/$', update_hit_count_ajax, name='hitcount_update_ajax'),
)
