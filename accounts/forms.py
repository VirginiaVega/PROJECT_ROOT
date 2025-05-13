from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


#Formulario para el registro de usuarios
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está registrado.")
        return username
    
    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return p2



#Formulario para edicion de usuarios
class UserEditForm(UserChangeForm):
    password = None 
    email = forms.EmailField(label="Correo electrónico", required=True)
    password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Repetir nueva contraseña', widget=forms.PasswordInput, required=False)
    class Meta: #esta clase trae el mail del usuario para verlo en pantalla
        model = User
        fields = ['email'] 
    def clean(self):#metodo de validacion de contraseñas
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 or p2:#compara
            if p1 != p2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=False) 
        if self.cleaned_data['password1']: 
            user.set_password(self.cleaned_data['password1']) #update usando set_password, guarda contraseña como HASH
        if commit: 
            user.save() 
        return user