from django.forms import ModelForm,Form
from django import forms
from .models import Franchises
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class FranchisesModelForm(ModelForm):
    class Meta:
        model = Franchises
        # fields = "__all__"
        # fields = ('f_name','f_nickname')
        exclude = ('f_logo',)

class FranchisesForm(Form):
    f_name = forms.CharField(max_length=30,required=True)
    f_nickname = forms.CharField(max_length=4,required=True)
    f_started_year = forms.IntegerField(required=True)
    f_logo = forms.ImageField(required=False)
    no_of_trophies = forms.IntegerField(required=True)

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('f_name', css_class='form-group col-md-6 mb-0'),
                Column('f_nickname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('f_started_year', css_class='form-group col-md-6 mb-0'),
                Column('no_of_trophies', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Column('f_logo',css_class='form-group col-md-6 mb-0'),
            Submit('submit','Submit')
        )