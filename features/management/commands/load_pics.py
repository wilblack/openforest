from django.core.management.base import BaseCommand, CommandError
from utils.client_managers import Droid

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Loads pics uploaded from my Android. Assumes pictures are located in /home/wilblack/android'
            
    def handle(self, *args, **options):
        dm=Droid()
        dm.load_pics()
        dm.assign_project()
    
           
