from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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