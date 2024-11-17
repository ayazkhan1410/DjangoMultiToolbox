from django.contrib import admin
from .models import *

@admin.register(Student)
class AdminStudent(admin.ModelAdmin):
    list_display = ['id', 'name', 'roll_number', 'age', 'std_class']
    list_filter = ['name']
    list_per_page = 10000

@admin.register(Employee)
class AdminEmployee(admin.ModelAdmin):
    list_display = ['employee_id', 'employee_name', 'designation', 'salary', 'retirement', 'other_benefits', 'total_benefits', 'total_compensation', ]
    search_fields = ['employee_name', 'designation']
    list_per_page = 5000

