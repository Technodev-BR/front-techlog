from controllers.login.authorized import operacoes_usuario
from controllers.login.auth import usuario_login_by_user_id

def context_operacoes(request):
    context = {}

    try:
        usuario_logado = usuario_login_by_user_id(request.user.id)
        context['context_operacoes'] = operacoes_usuario(usuario_logado)
    except:
        pass
    
    return context
