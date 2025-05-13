from django.urls import path
from accounts import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.login_request, name="login"),
    path('logout/',LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('register/',views.register, name='registro'),
    path('me/',views.editar_perfil, name='edit_profile'),
    path('profile/',views.mi_perfil, name='perfil'),
    path('about/',views.acercade, name='about'),
]