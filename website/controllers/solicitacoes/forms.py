from django.forms import ModelForm
from .models import SolicitacoesModel

class SolicitacaoForm(ModelForm):
    class Meta:
        model = SolicitacoesModel
        fields = "__all__"