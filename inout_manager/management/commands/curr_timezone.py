from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

class Command(BaseCommand):
    def handle(self, *args, **options):
        currTime = timezone.now()    
        print currTime
  
