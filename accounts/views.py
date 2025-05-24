from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm  
from aposts.models import Post
from django.contrib.auth import logout




# Create your views here.

@login_required(login_url='login')
def acercade(request):
	return render(request, "account/about.html")


@login_required(login_url='login')
def mi_perfil(request):
    user = request.user
    contexto= Post.objects.filter(user=user)
    return render(request, "account/profile.html", {'publicaciones':contexto})



#login
def login_request(request):
    if request.method == "POST": #se hizo click en enviar POST
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('publicacion_list')
    else:
        form = AuthenticationForm()#si recien ingresa a la pantalla del login muestra el form vacio GET   
    return render(request, "account/login.html", {"form": form})



#registrar usuario
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "account/register.html", {"form": form})


            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password1']

#editar perfil
@login_required(login_url='login')
def editar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, instance=usuario)
        if miFormulario.is_valid():
            miFormulario.save()
            logout(request)
            return redirect('login')
    else:
        miFormulario = UserEditForm(instance=usuario)
    return render(request, "account/edit_profile.html", {"mi_form": miFormulario, "usuario": usuario})