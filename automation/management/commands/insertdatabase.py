from django.core.management.base import BaseCommand
from automation.models import Student

class Command(BaseCommand):
    help = "This command will use to insert Data into a Database"
    
    def handle(self, *args, **kwargs):
        message = f"Data inserted successfully"
        error_message = "Data already exists.."
        dataset = [
            {"name": "John Doe", "roll_number": "127", "age": 20, "std_class": 10},
            {"name": "Jane Doe", "roll_number": "128", "age": 21, "std_class": 11},
            {"name": "John Smith", "roll_number": "129", "age": 22, "std_class": 12},
            {"name": "Jane Smith", "roll_number": "130", "age": 23, "std_class": 13},
        ]
        
        for data in dataset:
            roll_number = data['roll_number']
            std_class = data['std_class']
            
            existing_data = Student.objects.filter(roll_number=roll_number, std_class=std_class).exists()
            
            if not existing_data:
                Student.objects.create(
                    name=data['name'],
                    roll_number=data['roll_number'],
                    age=data['age'],
                    std_class=data['std_class']
                )
                self.stdout.write(self.style.SUCCESS(f"{data['name']} inserted successfully"))
            else:
                self.stderr.write(self.style.ERROR(f"{data['roll_number']} Roll Numbers already exists.."))
        