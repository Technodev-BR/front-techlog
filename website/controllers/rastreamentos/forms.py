from django.forms import ModelForm
from .models import RastreamentoModel

class RastreamentoForm(ModelForm):
    class Meta:
        model = RastreamentoModel
        fields = "__all__"
