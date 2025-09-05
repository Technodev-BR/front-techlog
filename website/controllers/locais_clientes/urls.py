from django.urls import path
from .models import *
from .views import *

app_name = 'locais_clientes'

urlpatterns = [
    path(r"buscar" ,buscar ,name="buscar"),
    path(r"cadastrar", cadastrar, name="cadastrar"),
    path(r"deletar/<int:id>/", deletar, name="deletar"),
    path(r"deletar_by_list_Id", deletar_by_list_Id, name="deletar_by_list_Id"),
    path(r"buscar_by_Id/<int:id>/", buscar_by_Id, name="buscar_by_Id"),
    path(r"buscar_by_local_Id/<int:id>/", buscar_by_local_Id, name="buscar_by_local_Id")
]