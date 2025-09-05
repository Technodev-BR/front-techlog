from django.forms import ModelForm
from controllers.clientes.models import ClienteModel

class ClienteForm(ModelForm):
    class Meta:
        model = ClienteModel
        fields = "__all__"