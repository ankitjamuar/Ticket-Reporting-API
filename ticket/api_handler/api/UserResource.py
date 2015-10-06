from tastypie.resources import ModelResource
from django.conf.urls import url
from tastypie.utils import trailing_slash, dict_strip_unicode_keys
from django.contrib.auth.models import User
from api_handler.models import Ticket, Message


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'


    def prepend_urls(self):
        return [
            url(r"^users/add-ticket/(?P<ticket_name>\w+)/$",
                self.wrap_view('add_ticket'), name="api_add_ticket"),

             url(r"^users/add-message/(?P<message>\w+)/$",
                self.wrap_view('add_message'), name="add_message")


            ]

    ######################################ALL THE FUNCTIONAL PART IS DEFINED BELOW ######################################


    # This API endpoint will return no of closed ticket within specified range
    def add_ticket(self, request, ticket_name, **kwargs):
        self.method_check(request, allowed=['get'])

        ticket = Ticket.objects.create(name=ticket_name)
        ticket.save()        

        return self.create_response(request, "Ticket Created Successfully!")


    # This API endpoint will return replytime within specified range
    def add_message(self, request, message, **kwargs):
        self.method_check(request, allowed=['get'])
        
        ticket = Message.objects.create(message=message, FK_ticket = Ticket(pk=1), FK_account=User(pk=4))
        ticket.save()  


        return self.create_response(request, ticket)