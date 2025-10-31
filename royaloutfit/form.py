from django import forms
from .models import WardrobeTable

class WardrobeForm(forms.ModelForm):
    class Meta:
        model = WardrobeTable
        fields = ['Name','Dress', 'model_name', 'dress_type', 'gendertype']
       
