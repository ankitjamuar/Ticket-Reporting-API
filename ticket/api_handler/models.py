from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Ticket(models.Model):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(default=datetime.now, blank=True)


    def save(self, *args, **kwargs):

        return super(Ticket, self).save(*args, **kwargs)



class Message(models.Model):
	message = models.TextField()
	updated = models.DateTimeField(default=datetime.now, blank=True)
	FK_ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
	FK_account = models.ForeignKey(User, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		return super(Message, self).save(*args, **kwargs)

