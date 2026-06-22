from django.shortcuts import render

# Create your views here.
from store.models import student_record

def func(request):
    data=student_record.objects.all()

    context={
        'data':data
    }

    return render(request, 'home.html', context)