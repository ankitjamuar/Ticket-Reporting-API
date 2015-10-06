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
    	allowed_methods = ['get']
        queryset = Ticket.objects.all()
        resource_name = 'medlanes'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/ticket-closed(?:/(?P<_from>\d{4}-\d{2}-\d{2}))?(?:/(?P<_to>\d{4}-\d{2}-\d{2}))?/$" %
                (self._meta.resource_name),
                self.wrap_view('ticket_closed'), name="api_ticket_closed"),

            url(r"^(?P<resource_name>%s)/ticket-replytime(?:/(?P<_from>\d{4}-\d{2}-\d{2}))?(?:/(?P<_to>\d{4}-\d{2}-\d{2}))?/$" %
                (self._meta.resource_name),
                self.wrap_view('ticket_replytime'), name="api_ticket-replytime"),

            url(r"^(?P<resource_name>%s)/ticket-closetime(?:/(?P<_from>\d{4}-\d{2}-\d{2}))?(?:/(?P<_to>\d{4}-\d{2}-\d{2}))?/$" %
                (self._meta.resource_name),
                self.wrap_view('ticket_closetime'), name="api_ticket-closetime"),

            url(r"^(?P<resource_name>%s)/ticket-status-series(?:/(?P<_from>\d{4}-\d{2}-\d{2}))?(?:/(?P<_to>\d{4}-\d{2}-\d{2}))?/$" %
                (self._meta.resource_name),
                self.wrap_view('ticket_status_series'), name="api_ticket_status_series"),

            url(r"^(?P<resource_name>%s)/ticket-replytime-series(?:/(?P<_from>\d{4}-\d{2}-\d{2}))?(?:/(?P<_to>\d{4}-\d{2}-\d{2}))?/$" %
                (self._meta.resource_name),
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

        # Get all the latest message  inside  tickets raised, if that message is from Expert that is closed
        latest_tickets = Ticket.objects.annotate(ticket_id = Max('message__id'))

        if _from is None or (_from is None and _to is None):
            
            m =  Message.objects.filter(id__in = [ ticket.ticket_id for ticket in latest_tickets], FK_account_id__is_staff=1).count()

        if _to is None and _from is not None:
            
            m =  Message.objects.filter(id__in = [ ticket.ticket_id for ticket in latest_tickets], FK_account_id__is_staff=1,updated__gte =_from).count()

        if _from is not None and _to is not None:

            m = Message.objects.filter(id__in = [ ticket.ticket_id for ticket in latest_tickets], FK_account_id__is_staff=1,updated__range=[_from,_to]).count()

     
        return self.create_response(request, m)


    # This API endpoint will return replytime within specified range
    def ticket_replytime(self, request, _from, _to, **kwargs):
        self.method_check(request, allowed=['get'])

        # Add 23hours 59 Minutes to reach midnight
        if _to is not None:
            _to = datetime.strptime(_to, "%Y-%m-%d") + timedelta(hours=23, minutes=59)


        second_message_time = None
        total_tickets = 0
        reply_time = 0

        '''
            Filter Tickets from Date Range

        '''
        if _from is None or (_from is None and _to is None):
            TICKETS = Ticket.objects.all()

        if _to is None and _from is not None:
            TICKETS = Ticket.objects.filter(updated__gte =_from)

        if _from is not None and _to is not None:
            TICKETS = Ticket.objects.filter(updated__range=[_from,_to])

        
        for ticket in TICKETS:           
            i = 0
            replytime = None
            first_message_time = None
            second_message_time = None

            
            '''
                Filter Messages from Date Range

            '''
            if _from is None or (_from is None and _to is None):
                MSGS = Message.objects.filter(FK_ticket_id=ticket.id)

            if _to is None and _from is not None:
                MSGS = Message.objects.filter(FK_ticket_id=ticket.id, updated__gte =_from)

            if _from is not None and _to is not None:
                MSGS = Message.objects.filter(FK_ticket_id=ticket.id, updated__range=[_from,_to])


            for message in MSGS:
                if i == 0:
                    first_message_time = message.updated
                    print first_message_time
                if i > 0:
                    expert_reply = User.objects.filter(pk=message.FK_account_id, is_staff =1 ).count()
                    if expert_reply == 1:
                        second_message_time = message.updated
                        total_tickets += 1
                        print second_message_time
                        break
                i += 1
            if second_message_time is not None:
                
                d = (second_message_time - first_message_time)

                reply_time +=   d.days * 24 * 60 * 60 + d.seconds  

                '''
                    Debugging Purpose
                    
                
                print "Ticket ID ", ticket.id
                print "Reply Time ", reply_time
                print "total_tickets", total_tickets
                print "Total Sum ", reply_time
                print "############################"
                '''
        if total_tickets > 0:
            avg_time = (reply_time/total_tickets)/3600
        else:
            avg_time = 0
            

        return self.create_response(request, avg_time)


    # This API endpoint will return ticket close time within specified range
    def ticket_closetime(self, request, _from, _to, **kwargs):
        self.method_check(request, allowed=['get'])

        # Add 23hours 59 Minutes to reach midnight
        if _to is not None:
            _to = datetime.strptime(_to, "%Y-%m-%d") + timedelta(hours=23, minutes=59)


        second_message_time = None
        total_tickets = 0
        reply_time = 0

        '''
            Filter Tickets from Date Range

        '''
        if _from is None or (_from is None and _to is None):
            TICKETS = Ticket.objects.filter(FK_ticket_id=ticket.id)

        if _to is None and _from is not None:
            TICKETS = Ticket.objects.filter(FK_ticket_id=ticket.id, updated__gte =_from)

        if _from is not None and _to is not None:
            TICKETS = Ticket.objects.filter(FK_ticket_id=ticket.id, updated__range=[_from,_to])


        for ticket in TICKETS:           
            i = 1
            replytime = None
            first_message_time = None
            second_message_time = None

            '''
                Filter Tickets from Date Range

            '''
            if _from is None or (_from is None and _to is None):
                MSGS = Message.objects.filter(FK_ticket_id=ticket.id)

            if _to is None and _from is not None:
                MSGS = Message.objects.filter(FK_ticket_id=ticket.id, updated__gte =_from)

            if _from is not None and _to is not None:
                MSGS = Message.objects.filter(FK_ticket_id=ticket.id, updated__range=[_from,_to])

            latest_tickets = Ticket.objects.annotate(ticket_id = Max('message__id')).filter(id=ticket.id)

            # Log message time for first Message and the last message if replied by EXPERT
            for message in MSGS:
                if i == 1:
                    first_message_time = message.updated
                
                '''
                    Check if the message.id is the last message for a given Ticket
                    Since the first message will always be raised by User so don't check for i > 0
                '''
                if latest_tickets[0].ticket_id == message.id:
                    expert_reply = User.objects.filter(pk=message.FK_account_id, is_staff =1 ).count()
                    if expert_reply == 1:
                        second_message_time = message.updated
                        total_tickets += 1

                i += 1

            # If Second Message is given by expert
            if second_message_time is not None:
                
                d = (second_message_time - first_message_time)            
                reply_time +=   d.days * 24 * 60 * 60 + d.seconds  

                '''
                    Debugging Purpose

                '''
                print "Ticket ID ",ticket.id
                print "Reply Time ", d.days * 24 * 60 * 60 + d.seconds  
                print "total_tickets", total_tickets
                print "Total Sum ", reply_time
                print "############################"
        if total_tickets != 0:
            avg_time = (reply_time/total_tickets)/3600
        else:
            avg_time = 0

        return self.create_response(request, avg_time)


   	# This API endpoint will return ticket series within specified range
    def ticket_status_series(self, request, _from, _to, **kwargs):
        self.method_check(request, allowed=['get'])


        # Set From and To date for all cases, if From is not set, then set it to very firts date same for To
        if _to is not None:
            _to = datetime.strptime(_to, "%Y-%m-%d") + timedelta(hours=23, minutes=59)
        else:
            _to = Message.objects.all().order_by("-id")[0].updated

        if _from is not None:
            _from = datetime.strptime(_from, "%Y-%m-%d") 
        else:
            _from = Message.objects.all().order_by("id")[0].updated

        _from_temp = _from 
        data = ""


        # Get all the latest message  inside  tickets raised, if that message is from Expert that is closed
        latest_tickets = Ticket.objects.annotate(ticket_id = Max('message__id'))

        if _from is not None and _to is not None:

            # Iterate over 24 hour interval
            while(_from_temp <= _to):
                _to_temp = _from_temp + timedelta(hours=23, minutes = 59)
                tickets_closed = Message.objects.filter(id__in = [ ticket.ticket_id for ticket in latest_tickets], FK_account_id__is_staff=1, updated__range=[_from,_to_temp]).count()
                tickets_open = Message.objects.filter(id__in = [ ticket.ticket_id for ticket in latest_tickets], FK_account_id__is_staff=0, updated__range=[_from,_to_temp]).count()
                data += str(_from_temp.strftime("%Y-%m-%d")) +","+ str(tickets_open) +","+str(tickets_closed)+";"
                _from_temp = _from_temp + timedelta(hours=24)
     

        return self.create_response(request, data)


    # This API endpoint will return replytime in series within specified range
    def ticket_replytime_series(self, request, _from, _to, **kwargs):
        self.method_check(request, allowed=['get'])
        # Set From and To date for all cases, if From is not set, then set it to very firts date same for To
        if _to is not None:
            _to = datetime.strptime(_to, "%Y-%m-%d") + timedelta(hours=23, minutes=59)
        else:
            _to = Message.objects.all().order_by("-id")[0].updated

        if _from is not None:
            _from = datetime.strptime(_from, "%Y-%m-%d") 
        else:
            _from = Message.objects.all().order_by("id")[0].updated

        _from_temp = _from 
        data = ""


        # Get all the latest message  inside  tickets raised, if that message is from Expert that is closed
        latest_tickets = Ticket.objects.annotate(ticket_id = Max('message__id'))

        if _from is not None and _to is not None:

            # Iterate over 24 hour interval
            while(_from_temp <= _to):
                _to_temp = _from_temp + timedelta(hours=23, minutes = 59)
                _last_5_day = _from_temp - timedelta(days=5)
                avg_time  = self.ticket_replytime(request,str(_last_5_day.strftime("%Y-%m-%d")), str(_from_temp.strftime("%Y-%m-%d")), **kwargs )
         
                data += str(_from_temp.strftime("%Y-%m-%d")) +","+ str(avg_time.content) +";"
                _from_temp = _from_temp + timedelta(hours=24)
     

        return self.create_response(request, data)


