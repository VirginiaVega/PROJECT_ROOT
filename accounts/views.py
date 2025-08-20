from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserEditForm, CustomAuthenticationForm #AuthenticationForm es el original de Django, personalice los msjes con este Custom
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from aposts.models import Post, Score
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Profile
from .forms import ProfileForm
# Create your views here.

#Explorar
@login_required(login_url='login')
def explore(request):
	return render(request, "account/explore.html")


#Editar datos, foto y descripcion
@login_required(login_url='login')
def edit(request, username):
    perfil_user = get_object_or_404(User, username=username)
    if perfil_user != request.user: #validar que el user que accede sea el logueado
        return redirect('perfil', username=request.user.username)    
    profile = perfil_user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('perfil', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "account/edit_data.html", {'perfil_user': perfil_user, 'form': form,})


#Perfil
@login_required(login_url='login')
def mi_perfil(request, username):
     perfil_user = get_object_or_404(User, username=username) 
     tipo = request.GET.get('tipo', 'posteos')  # 'posteos' por defecto
     if tipo == 'calificados' and perfil_user == request.user:
        publicaciones = [
            {"post": score.post, "score": score.score}
            for score in Score.objects.filter(user=request.user).select_related("post").order_by("-post__created_at")
        ]
     else:
        publicaciones = [{"post": p, "score": None} for p in Post.objects.filter(user=perfil_user)]
     return render(request, "account/profile.html",{'perfil_user': perfil_user, 'publicaciones': publicaciones, 'tipo': tipo})



#login
def login_request(request):
    if request.method == "POST": #se hizo click en enviar POST
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('publicacion_list')
    else:
        form = CustomAuthenticationForm()#si recien ingresa a la pantalla del login muestra el form vacio GET   
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


#editar perfil PSW MAIL
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