from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth.models import User

from . import serializers

@login_required
def get_active_users(request):
    context = {
        "users": User.objects.filter(is_active=True),
        "title": "Действующий штат",
        "page": "staff"
    }
    return render(request, "users/users_list.html", context)

@login_required
def get_prev_users(request):
    context = {
        "users": User.objects.filter(is_active=False),
        "title": "Раньше работали",
        "page": "past_staff"
    }
    return render(request, "users/users_list.html", context)

def login(request):
    return render(request, 'login.html')

@login_required
def profile(request):
    user = request.user
    return render(request, 'start.html', {'user':user})
