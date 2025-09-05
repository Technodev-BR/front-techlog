from django.contrib import admin
from django.urls import include, path
from controllers.usuarios.models import *
from controllers.usuarios.views import *
from controllers.clientes.models import *
from controllers.clientes.views import *
from controllers.iscas.models import *
from controllers.login.views import *
from controllers.rastreamentos.models import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path(r"",HomePage,name="home"),
    
    path(r"login/",LoginPage, name="login"),
    
    path(r"logout/",LogoutPage, name="logout"),
    
    path(r'usuarios/', include('controllers.usuarios.urls')),
    
    path(r'usuarios_operacoes/', include('controllers.usuarios_operacoes.urls')),
    
    path(r'iscas/', include('controllers.iscas.urls')),
    
    path(r'rastreamentos/', include('controllers.rastreamentos.urls')),
    
    path(r'solicitacoes/', include('controllers.solicitacoes.urls')),
    
    path(r'checklists/', include('controllers.checklists.urls')),
    
    path(r'clientes/', include('controllers.clientes.urls')),
    
    path(r'operacoes/', include('controllers.operacoes.urls')),
    
    path(r'locais/', include('controllers.locais.urls')),
    
    path(r'locais_clientes/', include('controllers.locais_clientes.urls')),
    
    path(r'fornecedores/', include('controllers.fornecedores.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

