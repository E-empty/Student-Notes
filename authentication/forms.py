from django import forms
from .models import Note
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from .models import MyGroup
from .models import Category

class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    
class GroupForm(forms.ModelForm):
    class Meta:
        model = MyGroup
        fields = ('name',)
        labels = {'name': 'Nazwa'}


class NoteForm(forms.ModelForm):
    delete_picture = forms.BooleanField(required=False)
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
        
class AddUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=None, label='Wybierz użytkownika:')

    def __init__(self, group_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_id = group_id
        self.fields['user'].queryset = get_user_model().objects.exclude(groups__id=group_id)

    def save(self):
        user = self.cleaned_data['user']
        group = MyGroup.objects.get(id=self.group_id)
        user.groups.add(group)
