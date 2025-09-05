from django.forms import ModelForm
from .models import UsuariosOperacaoModel

class UsuariosOperacaoForm(ModelForm):
    class Meta:
        model = UsuariosOperacaoModel
        fields = "__all__"