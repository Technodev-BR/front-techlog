from controllers.login.auth import usuario_login_by_user_id
from controllers.login.authorized import clientes_usuario

def context_clientes(request):
    context = {}
    
    try:
        usuario_logado = usuario_login_by_user_id(request.user.id)
        context['context_clientes'] = clientes_usuario(usuario_logado,True)
    except Exception as ex:
        print(ex)
        
    return context
