from django.forms import ModelForm
from .models import LocalModel

class LocalForm(ModelForm):
    class Meta:
        model = LocalModel
        fields = "__all__"
