from django.db import models

# Create your models here.
from django.core.validators import RegexValidator

class student_record(models.Model):
    stu_rollnumber=models.IntegerField(unique=True)
    stu_name=models.CharField(max_length=40)
    stu_class=models.CharField(max_length=6)
    gender=[
        ('male','MALE'),
        ('female','FEMALE'),
        ('others','OTHERS')
    ]
    stu_gender=models.CharField(max_length=11,choices=gender)
    regex_number=RegexValidator(r'[6-9][0-9]{9}')
    stu_mobile=models.CharField(max_length=10,validators=[regex_number])

    stu_image=models.ImageField(upload_to='images/')
    stu_markssheet=models.FileField(upload_to='files/')