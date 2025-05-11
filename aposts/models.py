from django.db import models
from django.contrib.auth.models import User
from .choises import  ESTRELLAS
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posteo', null=True, blank=True)  # Relación con el modelo User
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación
    image = models.ImageField(upload_to='entradas/', null=True, blank=True)  # Imagen opcional
    # Método para mostrar el título y el nombre de usuario al representar el objeto
    def __str__(self):
        return f'{self.title} - {self.user.username if self.user else "Anónimo"}'
    class Meta:
        ordering = ['-created_at']  # Ordenar por fecha de creación (de más reciente a más antiguo)

class Score(models.Model):
    score = models.CharField(max_length=1, choices=ESTRELLAS, default='1')    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='puntajes_posteo', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='puntajes_usuario', null=True, blank=True)
    def __str__(self):
        return f'{self.score} - {self.post.title} - {self.user.username if self.user else "Anónimo"}'
    class Meta:
        verbose_name = 'Puntaje'
        verbose_name_plural = 'Puntajes'

class Comment(models.Model):
    comment = models.TextField()  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')  # Relación con el modelo Post, para saber a qué publicación pertenece el comentario
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User, para saber qué usuario escribió el comentario
    created_at = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return f'{self.user.username}: {self.comment[:30]}...'  
    class Meta:
        verbose_name = 'Comentario' 
        verbose_name_plural = 'Comentarios'
        ordering = ['-created_at']  # Orden de los comentarios por fecha de creación, de más reciente a más antiguo
