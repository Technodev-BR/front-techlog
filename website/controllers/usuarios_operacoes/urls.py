from django.urls import path
from .models import *
from .views import *

app_name = 'usuarios_operacoes'

urlpatterns = [
    path(r"buscar", buscar, name="buscar"),
    path(r"cadastrar", cadastrar, name="cadastrar"),
    path(r"atualizar/<int:id>/", atualizar, name="atualizar"),
    path(r"deletar/<int:id>/", deletar, name="deletar"),
    path(r"buscar_by_Id/<int:id/", buscar_by_Id, name="buscar_by_Id")
]