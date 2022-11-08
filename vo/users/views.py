from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth.models import User

from . import serializers

def get_users(request):
    context = {
        "users": User.objects.all()
    }
    return render(request, "users/users_list.html", context)

def login(request):
    return render(request, 'login.html')

@login_required
def profile(request):
    user = request.user
    return render(request, 'start.html', {'user':user})

@login_required
def clients(request):
    context = {
        'user': request.user,
        'page': request.GET.get("page", 1)
    } 
    user = request.user
    print(user.groups.filter(name__in=['irk', 'angsk']).exists())    
    return render(request, 'clients_list.html', context=context)

@login_required
def client(request, pk):
    context = {
        'user': request.user,
        'pk': pk,
        'back_page': request.GET.get("back_page", 1)
    } 
    return render(request, 'client.html', context=context)

@login_required
def create_client(request):
    context = {
        'user': request.user,
        'back_page': request.GET.get("back_page", 1)
    } 
    return render(request, 'new_client.html', context=context)