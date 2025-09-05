from django.forms import ModelForm
from .models import OperacaoModel

class OperacaoForm(ModelForm):
    class Meta:
        model = OperacaoModel
        fields = "__all__"
