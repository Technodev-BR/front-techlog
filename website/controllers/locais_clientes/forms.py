from django.forms import ModelForm
from .models import LocaisClienteModel

class LocaisClienteForm(ModelForm):
    class Meta:
        model = LocaisClienteModel
        fields = "__all__"

