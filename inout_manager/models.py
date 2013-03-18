from django.db import models

class Expedition(models.Model):
    name = models.CharField(max_length=30)
    exped_id = models.IntegerField()

class Player(models.Model):
    exped = models.ForeignKey(Expedition)
    name = models.CharField(max_length=30)
    update_date = models.DateField()



# Create your models here.
