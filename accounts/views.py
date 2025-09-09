from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserEditForm, CustomAuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from aposts.models import Post, Score
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .forms import ProfileForm
from django.db.models import Sum, Value, Q
from django.db.models.functions import Coalesce
from datetime import datetime, timedelta
from django.contrib.auth import views as auth_views
from django.contrib import messages
# Create your views here.


#Mensaje personalizado al modificar Pswrd
class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        messages.success(request, '¡La contraseña se modifico con exito!')
        return redirect('login')


#Explore TOP y Random posts
@login_required(login_url='login')
def explore(request): 
    type = request.GET.get('type', 't')
    last_month = datetime.now().date() - timedelta(days=30) 
    if type == 't': #Posts order by Score
        posts= Post.objects.filter(created_at__date__gte=last_month).annotate(total_scores=Coalesce(Sum('puntajes_posteo__score'), Value(0))).filter(total_scores__gt=0).order_by('-total_scores')
    else: #Posts order by random
        #Scale
        posts= Post.objects.filter(created_at__date__gte=last_month).annotate(total_scores=Coalesce(Sum('puntajes_posteo__score'), Value(0))).filter(total_scores__gt=0).order_by('?')  
    context = {'posts': posts}
    return render(request, "account/explore.html", context)





#register user
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



#login
def login_request(request):
    if request.user.is_authenticated:
        return redirect('publicacion_list')  
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('publicacion_list')
    else:
        form = CustomAuthenticationForm()    
    return render(request, "account/login.html", {"form": form})


#edit profile: password and email (security)
@login_required(login_url='login')
def editProfileSecurity(request):
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


#Profile: own posts, other posts, score posts
#perfilConsultQualifsConsult()
@login_required(login_url='login')
def perfilConsult(request, username):
     perfil_user = get_object_or_404(User, username=username) 
     tipo = request.GET.get('tipo', 'posteos')
     if tipo == 'calificados' and perfil_user == request.user:
        publicaciones = [
            {"post": score.post, "score": score.score}
            for score in Score.objects.filter(user=request.user).select_related("post").order_by("-post__created_at")
        ]
     else:
        publicaciones = [{"post": p, "score": None} for p in Post.objects.filter(user=perfil_user)]
     return render(request, "account/profile.html",{'perfil_user': perfil_user, 'publicaciones': publicaciones, 'tipo': tipo})


#edit profile: avatar and description
@login_required(login_url='login')
def editProfile(request, username):
    perfil_user = get_object_or_404(User, username=username)
    if perfil_user != request.user:
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