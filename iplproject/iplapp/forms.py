from django.forms import ModelForm
from .models import Franchises

class FranchisesModelForm(ModelForm):
    class Meta:
        model = Franchises
        fields = "__all__"