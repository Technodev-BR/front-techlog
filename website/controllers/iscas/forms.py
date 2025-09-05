from django.forms import ModelForm
from .models import IscaModel

class IscaForm(ModelForm):
    class Meta:
        model = IscaModel
        fields = "__all__"