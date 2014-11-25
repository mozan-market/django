from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'karma.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'karma_app.views.public'), # root
    #url(r'^login$', 'karma_app.views.login_view'), # login
    #url(r'^logout$', 'karma_app.views.logout_view'), # logout
    #url(r'^signup$', 'karma_app.views.signup'), # signup
    #url(r'^posts$', 'karma_app.views.public'), # public posts
    #url(r'^submit$', 'karma_app.views.submit'), # submit new posts
    url(r'^users/$', 'karma_app.views.users'),
    url(r'^users/(?P<username>\w{0,30})/$', 'karma_app.views.users'),
    url(r'^follow$', 'karma_app.views.follow'),

)
  