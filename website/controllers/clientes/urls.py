from django.urls import path
from .models import *
from .views import *

app_name = 'clientes'

urlpatterns = [
    path(r"index", index, name="index"),
    path(r"buscar", buscar, name="buscar"),
    path(r"buscar_removidos" ,buscar_removidos ,name="buscar_removidos"),
    path(r"cadastrar", cadastrar, name="cadastrar"),
    path(r"atualizar/<int:id>/", atualizar, name="atualizar"),
    path(r"deletar/<int:id>/", deletar, name="deletar"),
    path(r"buscar_by_Id/<int:id>/", buscar_by_Id, name="buscar_by_Id")
]