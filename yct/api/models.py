from django.db import models
from django.contrib.auth.models import AbstractUser
import random, string

# Create your models here.
class SchoolUser(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    matric_no = models.CharField(max_length=20, null=True)
    staff_id = models.CharField(max_length=30, null=True)
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