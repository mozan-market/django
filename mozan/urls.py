from django.conf.urls import patterns, include, url
from django.contrib import admin
from mozan_app import views
from mozan_app.viewsets import UserViewSet, PostViewSet, ImageViewSet
from sms_signup.views import RegistrationApi, RegistrationView, ActivationView
from hitcount.views import update_hit_count_ajax
from rest_framework import routers
from rest_framework.authtoken import views as token_view


admin.autodiscover()


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'Users', UserViewSet)
router.register(r'Posts', PostViewSet)
router.register(r'Images', ImageViewSet)


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'mozan_app.views.public', name='home'), # root
    url(r'^user/(?P<username>\w{0,30})/$', 'mozan_app.views.users'),
    url(r'^post/(?P<post_id>\w{0,30})/$', 'mozan_app.views.posts'),
    url(r'^follow$', 'mozan_app.views.follow'),

    url(r'^api/registration/$', RegistrationApi.as_view(), name="registration"),
    url(r'^api/image/(?P<pk>\d+)$', views.ImageDetail.as_view(), name='image-detail'),
    url(r'^api/image/list/$', views.ImageList.as_view(), name='image-list'),
    url(r'^api/user/list/$', views.UserList.as_view(), name='user-list'),
    url(r'^api/user/(?P<pk>\d+)/$', views.UserDetail.as_view()),
    url(r'^api/user/(?P<pk>\d+)/profile$', views.UserProfileDetail.as_view()),

    url(r'^api/post/list/$', views.PostList.as_view(), name='post-list'),
    url(r'^api/post/(?P<pk>[0-9]+)/$', views.PostDetail.as_view()),
    url(r'^api/post/(?P<pk>\d+)/images/$', views.PostImageList.as_view(), name='postimage-list'),
    url(r'^api/auth/token/', token_view.obtain_auth_token),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/$', include(router.urls)),

    url(r'^search/', include('haystack.urls')),
    url(r'^counter/ajax/hit/$', update_hit_count_ajax, name='hitcount_update_ajax'),

    url(r'^sms/$', RegistrationView.as_view(), name="signup"),
    url(r'^activation/(?P<phone>[\d]{11,14})/$', ActivationView.as_view(), name="signup_activation"),

)
