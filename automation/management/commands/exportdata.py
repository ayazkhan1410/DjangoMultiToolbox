import csv
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import pytz  # Import pytz for timezone conversion
from django.apps import apps
from automation.helpers import generate_csv_filepath

 # propose Command : python manage.py exportdata modelname
class Command(BaseCommand):    
    help = "This command will export data from csv file and insert it into our Database"

    def add_arguments(self, parser):
        return parser.add_argument('model_name',type=str,help="Take Model name") 
       
    def handle(self, *args, **kwargs):
        try:
            model_name = kwargs['model_name'].capitalize()
                        
            # Search for the model across all the app
            for i in apps.get_app_configs():
                try:
                    model = apps.get_model(i.label, model_name)
                    break # stop searching if model found
                except LookupError:
                    continue # Continue for searching app
            
            if not model:
                raise CommandError(f"Model {model_name} not Found in any app")
                return
            
            # Fetch the data from the database
            data = model.objects.all()
            
            if not data.exists():
                self.stderr(self.style.ERROR("No Record Found.. "))
            
            # Generating File Path
            file_path = generate_csv_filepath(model_name)
                    
            # Opening the file and writing data
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                
                # write the CSV header
                # print all the model field according to model name
                writer.writerow([
                   field.name for field in model._meta.fields
                ])
                
                # Dynamically Writing Rows
                for item in data:
                    writer.writerow([
                        getattr(item,field.name) for field in model._meta.fields
                     ])
            
            self.stdout.write(self.style.SUCCESS(f"File Exported Successfully with the name of {file_path}"))
        except FileNotFoundError as file_not_found:
            print(file_not_found)
        except Exception as e:
            print("Exception: ",e)
            