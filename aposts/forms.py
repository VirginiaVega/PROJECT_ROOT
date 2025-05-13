from django import forms
from .models import Score, Comment


#Formulario para que puedan agregar puntaje a una publicacion
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score']  # Solo el campo de puntaje

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribí tu comentario...'}),
        }