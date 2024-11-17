from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This command will print Greeting message along with User name"
    
    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help="Greeting User with name")
        parser.add_argument('age',type=int, help="Printing Age")
    
    def handle(self, *args, **kwargs):
        greetings = kwargs['name']
        age = kwargs['age']
        final_result = f"Good Morning {greetings} sir! with age of {age}"
        self.stdout.write(self.style.SUCCESS(final_result))