
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    user = request.user
    return render(request, 'start.html', {'user':user})

@login_required
def clients(request):
    user = request.user
    return render(request, 'clients_list.html', {'user':user})

@login_required
def client(request, pk):
    user = request.user
    return render(request, 'client.html', {'user': user, 'pk': pk})