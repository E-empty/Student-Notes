from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    delete_picture = forms.BooleanField(required=False, label='Delete current picture')
    class Meta:
        model = Note
        fields = ['title', 'category', 'note', 'picture']
        widgets = {'category': forms.Select()}
        labels = {
            'title' : '',
            'category' : '',
            'note' : '',
            'picture' : '',
        }
