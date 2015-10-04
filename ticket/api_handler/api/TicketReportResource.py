from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from django.conf.urls import url
from tastypie.utils import trailing_slash, dict_strip_unicode_keys
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q, Max
from datetime import datetime, timedelta

# Models
from api_handler.models import Ticket, Message


class TicketReportResource(ModelResource):
    class Meta:
    	allowed_methods = []
        queryset = User.objects.all()
        resource_name = 'medlanes'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/ticket-closed(?:/(?P<_from>\d{4}-\d{2}-\d{2}))?(?:/(?P<_to>\d{4}-\d{2}-\d{2}))?/$" %
                (self._meta.resource_name),
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
    def ticket_closed(self, request, _from, _to, **kwargs):
        self.method_check(request, allowed=['get'])
        m = None
     
        # Get one messages from every Ticket raised whose date is MAX, it will be efficient
        # then getting all the messages that belongs to a EXPERT since ONE EXPERt can answer more that onnce in same ticket
        #qs = User.objects.all()
        #qs = qs.filter(Q(is_staff=True) & Q(is_superuser=False))

        # Add 23hours 59 Minutes to reach midnight
        if _to is not None:
            _to = datetime.strptime(_to, "%Y-%m-%d") + timedelta(hours=23, minutes=59)

        if _from is None or (_from is None and _to is None):
            
            m = Message.objects.values('FK_ticket_id').annotate(Max('updated')).filter(FK_account_id__is_staff=1).count()

        if _to is None and _from is not None:
            
            m = Message.objects.values('FK_ticket_id').annotate(Max('updated')).filter(FK_account_id__is_staff=1,updated__gte =_from).count()

        if _from is not None and _to is not None:

            m = Message.objects.values('FK_ticket_id').annotate(Max('updated')).filter(FK_account_id__is_staff=1,updated__range=[_from,_to]).count()

     
        return self.create_response(request, m)


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


