from django import forms

from .models.history import History
from .models.user import User
from .models.bot import TGBot

class HistoryForm(forms.ModelForm):
    message = forms.CharField(label='Текст сообщения или адрес картинки/документа', max_length=5000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
    class Meta:
        model = History
        fields = ['message']