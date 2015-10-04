from django.conf.urls import include, url
from django.contrib import admin
from tastypie.api import Api
from resources.UserResource import UserResource
from resources.TicketReportResource import TicketReportResource


# Hook Up the resources here
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(TicketReportResource())


urlpatterns = [
	
	url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
]
