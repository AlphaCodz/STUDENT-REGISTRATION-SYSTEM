from django.db import models
from django.contrib.auth.models import AbstractUser
import random, string

# Create your models here.


class Department(models.Model):
    DEPARTMENT = (
        ("COMPUTER SCIENCE", "COMPUTER SCIENCE"),
        ("BUSINESS ADMIN", "BUSINESS ADMIN"),
        ("ACCOUNTING", "ACCOUNTING"),
        ("MASS COMMUNICATION", "MASS COMMUNICATION"),
        ("OFFICE TECHNOLOGY MANAGEMENT", "OFFICE TECHNOLOGY MANAGEMENT"),
        ("POLYMER & TEXTILE", "POLYMER & TEXTILE"),
        ("MARKETING", "MARKETING"),
        ("SCIENCE & LABORATORY TECHNOLOGY", "SCIENCE & LABORATORY TECHNOLOGY")
    )
    
    department = models.CharField(max_length=50, choices=DEPARTMENT, null=True)
    
    def __str__(self):
        return self.department
    
class PROGRAMME(models.Model):
    PROGRAMME = (
        ("ND PART-TIME", "ND PART-TIME"),
        ("ND FULL-TIME", "ND FULL-TIME"),
        ("HND PART-TIME", "HND PART-TIME"),
        ("HND FULL-TIME", "HND FULL-TIME")
    )
    
    programme = models.CharField(max_length=13, choices=PROGRAMME, null=True)
    
    def __str__(self):
        return self.programme
    
class Session(models.Model):
    SESSION = (
        ("2019/2020", "2019/2020"),
        ("2020/2021", "2020/2021"),
        ("2021/2022", "2021/2022"),
        ("2022/2023", "2022/2023")
    )
    
    session = models.CharField(max_length=9, choices=SESSION, null=True)
    
    def __str__(self):
        return self.session
    
class Level(models.Model):
    LEVEL = (
        ("ND 1", "ND 1"), 
        ("ND 2", "ND 2"),
        ("ND 3", "ND 3"),
        ("HND 1", "HND 1"),
        ("HND 2", "HND 2")
    )
    
    level = models.CharField(max_length=5, choices=LEVEL, null=True)
    def __str__(self):
        return self.level
    
    
class SchoolUser(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    matric_no = models.CharField(max_length=20, null=True)
    staff_id = models.CharField(max_length=30, null=True)
    date_of_birth = models.DateField(null=True)
    home_address = models.CharField(max_length=150, null=True)
    programme = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, related_name="programmes")
    school=models.CharField(max_length=50, null=True)
    department= models.OneToOneField(Department, on_delete=models.PROTECT, null=True)
    level = models.ForeignKey(Level, on_delete=models.PROTECT, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    place_of_birth = models.CharField(max_length=10, null=True)
    state_of_origin = models.CharField(max_length=10, null=True)
    local_government_area = models.CharField(max_length=50, null=True)
    parent_name = models.CharField(max_length=150, null=True)
    parent_address = models.CharField(max_length=200, null=True)
    parent_contact = models.CharField(max_length=15, null=True)
    is_bursar = models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    is_course_adviser=models.BooleanField(default=False)
    
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]
    
    def __str__(self):
        return self.first_name
    
    def save(self, *args, **kwargs):
        random_usernames = "".join(random.choices(string.ascii_letters + string.digits, k=5))
        if not self.username:
            self.username = random_usernames
            super(SchoolUser, self).save(*args, **kwargs)
    
            
class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=5, null=True)
    
            
class CourseForm(models.Model):
    student = models.ForeignKey(SchoolUser, on_delete=models.PROTECT, related_name="course_forms", null=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, null=True)
    
    