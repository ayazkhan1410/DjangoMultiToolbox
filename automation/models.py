from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False)
    roll_number = models.CharField(max_length=255,null=False,blank=False)
    age = models.IntegerField(null=True,blank=True)
    std_class = models.IntegerField(null=False,blank=False)
    
    def __str__(self):
        return f"{self.name} - {self.roll_number}"
    
    class Meta:
        ordering = ['id']
    
    
class Employee(models.Model):
    employee_id = models.IntegerField()
    employee_name = models.CharField(max_length=255,null=False,blank=False)
    designation = models.CharField(max_length=3, null=True,blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=False,blank=False)
    retirement = models.DecimalField(max_digits=10, decimal_places=2,null=False,blank=False)
    other_benefits = models.DecimalField(max_digits=10, decimal_places=2,null=False,blank=False)
    total_benefits = models.DecimalField(max_digits=10, decimal_places=2,null=False,blank=False)
    total_compensation = models.DecimalField(max_digits=10, decimal_places=2,null=False,blank=False)
    
    def __str__(self):
        return f"{self.employee_name} - {self.designation}" 
    
    class Meta:
        ordering = ['employee_id']