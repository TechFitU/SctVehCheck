from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
import vehiclecheck.urls
import profiles.urls
import accounts.urls
from . import views

import hello.views
admin.autodiscover()
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    #path(r'^home/$', hello.views.index, name='index'),
    #path(r'^db/', hello.views.db, name='db'),
    path('hello/', hello.views.index, name='index'),
    path('db/', hello.views.db, name='db'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('users/', include(profiles.urls)),
    path('account/', include(accounts.urls)),

    # include the django-ajax-selects lookup urls
    path('admin/lookups/', include('ajax_select.urls')),
    path('chaining/', include('smart_selects.urls')),
    #django-simple-captcha urls
    #url(r'^captcha/', include('captcha.urls')),

    # include the vehiclecheck urls
    path('vehiclecheck/', include(vehiclecheck.urls)),

    url(r'^adminactions/', include('adminactions.urls')),
    #url(r'^admin/', admin_site.urls),
    path('admin/', admin.site.urls),
]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
