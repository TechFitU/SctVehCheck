import accounts.urls
import hello.views
import profiles.urls
import vehiclecheck.urls
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

admin.autodiscover()
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    #path(r'^home/$', hello.views.index, name='index'),
    #path(r'^db/', hello.views.db, name='db'),
    path('hello/', hello.views.index, name='index'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('users/', include(profiles.urls)),
    path(r'account/', include(accounts.urls)),

    # include the django-ajax-selects lookup urls
    path('admin/lookups/', include('ajax_select.urls')),
    path('chaining/', include('smart_selects.urls')),
    #django-simple-captcha urls
    #url(r'^captcha/', include('captcha.urls')),

    # include the vehiclecheck urls
    path('vehiclecheck/', include(vehiclecheck.urls)),

    url(r'^adminactions/', include('adminactions.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

# Serving static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
