from typing import Union
from django.contrib.auth import login,logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from controllers.login.auth import usuario_login_by_user_id

@login_required
def HomePage(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    usuario = usuario_login_by_user_id(request.user.id)
    if not usuario:
        logout(request)
        return redirect('login')
    
    context = {
       
        "titulo_page": "Bem Vindo",
    }
    return render(request, "pages/home.html", context)

def LoginPage(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    form = AuthenticationForm(request,data=request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():    
            user = form.get_user() 
            login(request, user)
            return redirect('home')
            
    context = {
        'form':form,
        'request':request.method
    }   
    return render(request, "pages/login.html", context)

def LogoutPage(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    logout(request)
    return redirect('login')