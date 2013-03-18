from django.core.management.base import BaseCommand, CommandError
from inout_manager.models import *
from inout_manager.archeage_crawler import run

class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
  
