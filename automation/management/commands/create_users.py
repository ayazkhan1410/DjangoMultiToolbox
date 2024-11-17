from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = "This command will Create Users"
    
    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        
        for i in range(1,total+1):
            User.objects.create_user(username=get_random_string(6),email = "ayazkhan1310@gmail.com", password='123')
            self.stdout.write("User Created Successfully")
            