from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Users

class Student(models.Model):
    student_id=models.AutoField(primary_key=True)
    course_id=models.IntegerField(null=True,blank=True)
    name=models.CharField(max_length=100)
    dob=models.DateField()
    gender=models.CharField(max_length=20)
    profile_pic=models.ImageField(null=True,blank=True)
    mobile_no=PhoneNumberField(null=False,blank=False,unique=True)
    email=models.EmailField()
    admission_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,default="Active")
    username=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=100)
    table_status=models.IntegerField(default=1)
    updated_at=models.DateTimeField(auto_now_add=True)

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=20)
    profile_pic = models.ImageField(null=True, blank=True)
    mobile_no = PhoneNumberField(null=False, blank=False, unique=True)
    skills=models.TextField()
    status = models.CharField(max_length=20, default="Active")
    wage=models.IntegerField()
    table_status = models.IntegerField(default=1,null=True,blank=True)
    username = models.CharField(max_length=100, unique=True)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Admin(models.Model):
    admin_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    username=models.CharField(max_length=100,unique=True)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)

# Courses

class Core_course(models.Model):
    course_id=models.AutoField(primary_key=True)
    staff_id=models.IntegerField(null=True,blank=True)
    course_name=models.CharField(max_length=20)
    description=models.TextField()
    duration=models.IntegerField()
    thumbnail=models.ImageField(null=True,blank=True)
    fees=models.IntegerField()
    table_status=models.IntegerField(default=1,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

# Fees

class Calc_fees(models.Model):
    fee_id=models.AutoField(primary_key=True)
    student_id = models.IntegerField(null=True, blank=True)
    course_id = models.IntegerField(null=True, blank=True)
    course_name=models.CharField(max_length=20,null=True, blank=True)
    extra_fees=models.IntegerField(default=0,null=True, blank=True)
    fee_details=models.TextField(null=True,blank=True)
    total_fee=models.IntegerField()
    payment=models.CharField(max_length=20,default="completed")
    table_status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

# Salary

class Salary(models.Model):
    salary_id=models.AutoField(primary_key=True)
    staff_id=models.IntegerField(null=True,blank=True)
    total_hrs=models.IntegerField()
    worked_hrs=models.IntegerField()
    bonus=models.IntegerField(null=True,blank=True)
    total_salary=models.IntegerField()
    status=models.CharField(max_length=20,default='received')
    table_status=models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

# Contact Page

class Contact(models.Model):
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_subject = models.TextField()
