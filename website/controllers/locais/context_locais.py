from controllers.login.auth import usuario_login_by_user_id
from controllers.login.authorized import locais_usuario

def context_locais(request):
    context = {}
       
    try:
        usuario_logado = usuario_login_by_user_id(request.user.id)
        context['context_locais'] = locais_usuario(usuario_logado,True)
    except Exception as ex:
        print(ex)
        
    return context
