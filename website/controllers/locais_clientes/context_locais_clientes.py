from controllers.login.auth import usuario_login_by_user_id
from controllers.login.authorized import locais_clientes_usuario

def context_locais_clientes(request):
    context = {}
       
    try:
        usuario_logado = usuario_login_by_user_id(request.user.id)
        context['context_locais_clientes'] = locais_clientes_usuario(usuario_logado)
    except Exception as ex:
        print(ex)
        
    return context
