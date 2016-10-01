from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from app.views import *
from app.forms import RegisterForm


admin.site.site_title = 'FIBRANDO'
admin.site.site_index = 'FIBRANDO'
admin.site.site_header = 'DASHBOARD'

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/edit/'


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #django-admin urls
    url(r'^admin/', include(admin.site.urls)),

    #registration urls
    url(r'accounts/register/$', MyRegistrationView.as_view(form_class = RegisterForm),
        name = 'registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    #my apps urls
    url(r'^', include('app.urls')),
    url(r'^api/', include('api.urls')),

)


if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
