from django.urls import path
from .models import *
from .views import *

app_name = 'checklists'

urlpatterns = [
    path(r"buscar", buscar, name="buscar"),
    path(r"buscar_by_Id/<int:id/", buscar_by_Id, name="buscar_by_Id"),
    path(r"cadastrar", cadastrar, name="cadastrar"),
    path(r"email_checklist", email_checklist, name="email_checklist"),
]