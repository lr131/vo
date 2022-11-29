from django.shortcuts import render, redirect
from .forms import ClientEventHistoryForm
from .models import  ClientEventHistory

def add_visit(request):
    if request.method == "POST":
        form = ClientEventHistoryForm(request.POST)
        if form.is_valid():
            print(form)
            history = form.save()
            return redirect('crm:get_list')
    else:
        context = {
            "form": ClientEventHistoryForm()
        }
    return render(request, "crm/add_visit.html", context)

def get_list(request):
    context = {
        "histories": ClientEventHistory.objects.all()
    }
    return render(request, "crm/history.html", context)