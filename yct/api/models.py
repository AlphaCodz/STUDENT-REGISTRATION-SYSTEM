from django.db import models
from django.contrib.auth.models import AbstractUser
import random, string

# Create your models here.
class SchoolUser(AbstractUser):
    PROGRAMME = (
        ("ND PART-TIME", "ND PART-TIME"),
        ("ND FULL-TIME", "ND FULL-TIME"),
        ("HND PART-TIME", "HND PART-TIME"),
        ("HND FULL-TIME", "HND FULL-TIME")
    )
    
    SESSION = (
        ("2019/2020", "2019/2020"),
        ("2020/2021", "2020/2021"),
        ("2021/2022", "2021/2022"),
        ("2022/2023", "2022/2023")
    )
    
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
    
    LEVEL = (
        ("ND 1", "ND 1"), 
        ("ND 2", "ND 2"),
        ("ND 3", "ND 3"),
        ("HND 1", "HND 1"),
        ("HND 2", "HND 2")
    )
    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    matric_no = models.CharField(max_length=20, null=True)
    staff_id = models.CharField(max_length=30, null=True)
    date_of_birth = models.DateField(null=True)
    home_address = models.CharField(max_length=150, null=True)
    programme = models.CharField(max_length=13, choices=PROGRAMME, null=True)
    school=models.CharField(max_length=50, null=True)
    department= models.CharField(max_length=50, choices=DEPARTMENT, null=True)
    level = models.CharField(max_length=5, choices=LEVEL, null=True)
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