from django.contrib import admin

# Register your models here.
from store.models import student_record

class student_admin(admin.ModelAdmin):
    list_display=['stu_rollnumber','stu_name','stu_class','stu_mobile','stu_gender','stu_image','stu_markssheet']

admin.site.register(student_record,student_admin)