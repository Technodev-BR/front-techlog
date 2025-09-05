from django.urls import path
from .models import *
from .views import *

app_name = 'solicitacoes'

urlpatterns = [
    path(r"index" ,index ,name="index"),
    path(r"buscar", buscar, name="buscar"),
    path(r"buscar_removidos" ,buscar_removidos ,name="buscar_removidos"),
    path(r"buscar_by_Id/<int:id>/", buscar_by_Id, name="buscar_by_Id"),
    path(r"cadastrar_range", cadastrar_range, name="cadastrar_range"),
    path(r"deletar/<int:id>/", deletar, name="deletar"),
    path(r"atualizar_checkout/<int:id>/", atualizar_checkout, name="atualizar_checkout"),
    path(r"atualizar_checkin/<int:id>/", atualizar_checkin, name="atualizar_checkin")
]