from django.forms import ModelForm
from django import forms
from .models import NewEntry

class EntryForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ' Title', 'class': 'Form-Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'Form-Content'}))
    class Meta:
        model = NewEntry
        fields = ('title', 'description')  

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ' Title', 'class': 'Form-Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'Form-Content'}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)