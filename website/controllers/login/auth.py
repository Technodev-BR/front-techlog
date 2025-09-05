from controllers.usuarios.models import UsuarioModel,ROLES
    
def usuario_login_by_user_id(user_id : int):
    try:
        usuario_login = UsuarioModel.objects.get(user=user_id,ativo=True)
        return usuario_login 
    except Exception as ex:
        pass
    

def supervisor(usuario : UsuarioModel):
    try:
        if(usuario.roles == ROLES['SUPERVISOR']):
            return True
    except Exception as ex:
        print(ex)
    return False
    
def administrador(usuario : UsuarioModel):
    try:
        if(usuario.roles == ROLES['ADMINISTRADOR']):
            return True
    except Exception as ex:
        print(ex)
    return False
  
def administrador_or_supervisor(usuario : UsuarioModel):
    try:
        if(usuario.roles == ROLES['SUPERVISOR'] or usuario.roles == ROLES['ADMINISTRADOR']):
            return True
    except Exception as ex:
        print(ex)
    return False