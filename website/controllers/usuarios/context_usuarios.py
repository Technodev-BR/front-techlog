from controllers.login.auth import usuario_login_by_user_id
from controllers.usuarios.models import ROLES
from controllers.iscas.models import MODELOS

def context_usuarios(request):
    context = {}
    
    try:
        
        usuario_login = usuario_login_by_user_id(request.user.id)
        usuario_login.foto = usuario_login.foto.name == '' and '/assets/img/userDefault.svg' or usuario_login.foto.url
        context['context_usuarios'] = usuario_login
        context['ROLES'] = ROLES
        context['context_modelos'] = MODELOS
        
    except Exception as ex:
        print(ex)
        
    return context