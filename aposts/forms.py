from django import forms
from .models import Score, Comment
from .choises import  STARS


#Formulario para que puedan agregar puntaje a una publicacion
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score']
        widgets = {
            'score': forms.Select(choices=STARS)  # Usa las mismas choices
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribí tu comentario...'}),
        }