from django.forms import ModelForm
from .models import FornecedorModel

class FornecedorForm(ModelForm):
    class Meta:
        model = FornecedorModel
        fields = "__all__"
