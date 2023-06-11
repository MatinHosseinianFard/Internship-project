from django.shortcuts import render
from django.contrib.auth import get_user_model

def about_us(request):
    User = get_user_model()
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'about_us.html', context)
