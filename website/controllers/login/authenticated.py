from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from .auth import usuario_login_by_user_id

User = get_user_model()

class AuthenticatedBackend(BaseBackend):
    
    def authenticate(self, request: HttpRequest, username: str | None = ..., password: str | None = ..., **kwargs: Any):
        try: 
            user = User.objects.get(username=username,is_active=True)
            if user.check_password(password):
                usuario_login = usuario_login_by_user_id(user.id) 
                if(usuario_login):
                    user.detalhes = usuario_login
                return user
        except User.DoesNotExist:
            return None
         
    def get_user(self, user_id: int):
        try:
            user = User.objects.get(pk=user_id,is_active=True)
            usuario_login = usuario_login_by_user_id(user.id) 
            if(usuario_login):
                user.detalhes = usuario_login
            return user
        except User.DoesNotExist:
            return None