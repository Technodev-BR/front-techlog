from django.forms import ModelForm
from .models import UsuarioModel

class UsuarioForm(ModelForm):
    class Meta:
        model = UsuarioModel
        fields = "__all__"
       