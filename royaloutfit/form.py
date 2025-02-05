from django import forms
from .models import WardrobeTable

class WardrobeForm(forms.ModelForm):
    class Meta:
        model = WardrobeTable
        fields = ['Dress', 'model_name', 'dress_type']
       
