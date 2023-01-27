from django import forms
from physioweb.models import *
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.helper import FormHelper

class UserForm(forms.ModelForm):
    user = forms.CharField(max_length = 50)
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
        'password': forms.PasswordInput(),
    }
        
class GeneName(forms.Form):
    gene_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':"form-control mb-2",
            'list':'gene_names'
        }))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('gene_name', css_class='form-control mb-2'),
                Column(Submit('submit', 'Select')),
                css_class='form-inline'
                )
                )