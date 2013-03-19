from django.db import models

class Expedition(models.Model):
    name = models.CharField(max_length=30)
    exped_id = models.IntegerField()
    update_time = models.DateTimeField()
    inserted_time = models.DateTimeField()

class Player(models.Model):
    exped = models.ForeignKey(Expedition, null=True)
    name = models.CharField(max_length=30)
    update_time = models.DateTimeField()
    inserted_time = models.DateTimeField()



# Create your models here.
