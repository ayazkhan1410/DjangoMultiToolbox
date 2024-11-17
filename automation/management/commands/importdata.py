from django.core.management.base import BaseCommand,CommandError
import csv
from django.apps import apps
from django.db import DataError
from automation.helpers import check_csv_errors

# Proposed Command --> python manage.py importdata filepath + model name
class Command(BaseCommand):
    help = "This command will import data from csv File"
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Importing Data")
        parser.add_argument('model_name', type=str, help="Takes Model Name")
    
    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
        
        # Call the function
        model = check_csv_errors(file_path,model_name)
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for data in reader:
                model.objects.create(**data)
        self.stdout.write(self.style.SUCCESS("Data imported from csv successfully ..."))   
