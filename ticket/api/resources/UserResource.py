from tastypie.resources import ModelResource
from django.contrib.auth.models import User
#from api.models import UserModel


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'