from django.forms import ModelForm
from .models import ChecklistModel

class ChecklistForm(ModelForm):
    class Meta:
        model = ChecklistModel
        fields = "__all__"
