from django.urls import path
from .models import *
from .views import *

app_name = 'rastreamentos'

urlpatterns = [
    path(r"index" ,index ,name="index"),
    path(r"buscar", buscar, name="buscar"),
    path(r"buscar_removidos", buscar_removidos, name="buscar_removidos"),
    path(r"buscar_by_Id/<int:id>/", buscar_by_Id, name="buscar_by_Id"),
    path(r"buscar_by_isca_Id/<int:id>/", buscar_by_isca_Id, name="buscar_by_isca_Id"),
    path(r"atualizar/<int:id>/", atualizar, name="atualizar"),
    path(r"iniciar_rastreio/<int:id>/", iniciar_rastreio, name="iniciar_rastreio"),
    path(r"deletar_range" ,deletar_range ,name="deletar_range"),
    path(r"cadastrar" ,cadastrar ,name="cadastrar"),
]
