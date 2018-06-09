from django.conf.urls import url
from vehiclecheck import views
urlpatterns = [
    # include the django-ajax-selects lookup urls
    url(r'^last_verification/vehicle/(?P<identificador>[0-9a-zA-Z]+)/$', views.get_lastverification_by_vehicle, \
    	name="get_lastverification_by_vehicle"),

    url(r'^verification/(?P<identificador>[0-9a-zA-Z]+)/$', views.show_verification, \
    	name="show_verification"),
]
