from django.shortcuts import render

from .forms import MailingForm

def mailing_new(request):
    if request.method == "POST":
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            # mailing.author = request.user
            # mailing.published_date = timezone.now()
            mailing.save()
    else:
        form = MailingForm()
    return render(request, 'smm/mailing/mailing_new.html', {'form': form})

