from django.db import models

class Expedition(models.Model):
    name = models.CharField(max_length=30)
    exped_id = models.IntegerField()
    update_time = models.DateTimeField()
    inserted_time = models.DateTimeField()
    def __repr__(self):
        return ("%s, %s, %s, %s" % (self.name, self.exped_id, self.update_time, self.inserted_time)).encode('utf8')


class Player(models.Model):
    exped = models.ForeignKey(Expedition, null=True)
    name = models.CharField(max_length=30)
    update_time = models.DateTimeField()
    inserted_time = models.DateTimeField()
    prev_record = models.OneToOneField('Player', null=True)
    def __repr__(self):
        return ('%s, %s, %s, %s' % (self.name, self.exped.name if self.exped is not None else '-' , self.update_time, self.inserted_time)).encode('utf8')



# Create your models here.
