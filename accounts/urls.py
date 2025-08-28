from django.urls import path
from accounts import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.login_request, name="login"),
    path('logout/',LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('register/',views.register, name='registro'),
    path('me/',views.editar_perfil, name='edit_profile'),
    path('profile/<str:username>/',views.mi_perfil, name='perfil'),#espera un parametro username
    path('edit/<str:username>/',views.edit, name='edit'),
    path('explore/',views.explore, name='explore'),


    #2 para recuperacion de password
    path("password_reset/",auth_views.PasswordResetView.as_view(template_name="account/password_reset.html", email_template_name="account/password_reset_email.html", subject_template_name="account/password_reset_subject.txt") ,name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]