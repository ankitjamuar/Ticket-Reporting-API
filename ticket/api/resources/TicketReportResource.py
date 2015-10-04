from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from django.conf.urls import url
from tastypie.utils import trailing_slash, dict_strip_unicode_keys

# Models
from api.models import UserModel
from api.models import TicketModel


class TicketReportResource(ModelResource):
    class Meta:
    	allowed_methods = []
        queryset = User.objects.all()
        resource_name = 'medlanes'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/ticket-closed%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('ticket_closed'), name="api_ticket_closed"),

            url(r"^(?P<resource_name>%s)/ticket-replytime%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('ticket_replytime'), name="api_ticket-replytime"),

            url(r"^(?P<resource_name>%s)/ticket-closetime%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('ticket_replytime'), name="api_ticket-closetime"),

            url(r"^(?P<resource_name>%s)/ticket-status-series%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('ticket_status_series'), name="api_ticket_status_series"),

            url(r"^(?P<resource_name>%s)/ticket-replytime-series%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('ticket_replytime_series'), name="api_ticket_replytime_series")


            ]

    ######################################ALL THE FUNCTIONAL PART IS DEFINED BELOW ######################################


    # This API endpoint will return no of closed ticket within specified range
    def ticket_closed(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        print type(request)

        return self.create_response(request, request.REQUEST)


    # This API endpoint will return replytime within specified range
    def ticket_replytime(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        print request

        return self.create_response(request, request)


    # This API endpoint will return ticket close time within specified range
    def ticket_closetime(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        print request

        return self.create_response(request, request)


   	# This API endpoint will return ticket series within specified range
    def ticket_status_series(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        print request

        return self.create_response(request, request)

    # This API endpoint will return replytime in series within specified range
    def ticket_replytime_series(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        print request

        return self.create_response(request, request)


