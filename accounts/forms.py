from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Profile


#User registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", required=True, error_messages={'invalid': 'Introduzca una dirección de correo electrónico válida. user register'})
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Nombre de usuario no disponible.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email
    
    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return p2


#User edit form
class UserEditForm(UserChangeForm):
    password = None 
    email = forms.EmailField(label="Correo electrónico", required=True, error_messages={'invalid': 'Introduzca una dirección de correo electrónico válida. user edit'})
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Validar', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['email'] 

    def clean(self):#validate
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
            try:
                validate_password(p1, self.instance)
            except ValidationError as e:
                for msg in e.messages:
                    self.add_error('password1', msg)
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False) 
        if self.cleaned_data['password1']: 
            user.set_password(self.cleaned_data['password1']) 
        if commit: 
            user.save() 
        return user



class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Datos incorrectos. Verificar."
        ),
        'inactive': ("Esta cuenta está inactiva."),
    }


#Profile edit form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'avatar']


