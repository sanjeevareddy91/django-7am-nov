from django.forms import ModelForm,Form
from django import forms
from .models import Franchises

class FranchisesModelForm(ModelForm):
    class Meta:
        model = Franchises
        fields = "__all__"

class FranchisesForm(Form):
    f_name = forms.CharField(max_length=30,required=True)
    f_nickname = forms.CharField(max_length=4,required=True)
    f_started_year = forms.IntegerField(required=True)
    f_logo = forms.ImageField(required=False)
    no_of_trophies = forms.IntegerField(required=True)
