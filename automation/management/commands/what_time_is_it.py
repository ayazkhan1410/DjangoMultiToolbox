from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = "This command will print TimeZone"
    
    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)