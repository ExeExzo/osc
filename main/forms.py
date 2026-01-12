from django import forms
from .models import Camper

class CamperRegistrationForm(forms.ModelForm):
    class Meta:
        model = Camper
        fields = ['parent_id', 'uploaded_id']
        widgets = {
            'parent_id': forms.TextInput(attrs={'placeholder': 'ФИО родителя'}),
        }
