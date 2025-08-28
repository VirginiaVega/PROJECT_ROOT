# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from aposts.models import Post, Comment
from .forms import ScoreForm, CommentForm
from accounts.models import Profile
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, Count, Case, When, IntegerField
#PARA JS
from django.core.files.base import ContentFile
import base64, uuid



#Buscar
@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    resultados = []    
    if query:        # Búsqueda adaptada al modelo Profile
        resultados = (Profile.objects.filter(Q(user__username__icontains=query)).select_related('user').annotate(total_posts=Count('user__posteo'), 
                    start=Case(When(user__username__istartswith=query, then=1), default=0, output_field=IntegerField())).order_by('-start', '-total_posts'))[:12]  # limita a 12 resultados
    context = {'resultados': resultados, 'query': query}        
    return render(request, "aposts/search.html", context)


#Eliminar comentario
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user:
        return redirect('publicacion_detail', pk=comment.post.pk)  # <-- redirige al detalle si el comentario no es suyo
    post_pk = comment.post.pk  # guardamos el id de la publicación antes de borrar
    comment.delete()
    return redirect('publicacion_detail', pk=post_pk)  # <-- vuelve al detalle



#Crea sin agregar el puntaje, pero si agregando el usuario
class PublicacionCrear(LoginRequiredMixin, CreateView):
    model=Post
    template_name='aposts/post_form.html'
    success_url=reverse_lazy('publicacion_list')
    fields=['title','body', 'image']    
    #Asigna el usuario y recorta la imagen
    def form_valid(self, form):
        form.instance.user=self.request.user #Toma el usuario para guarar la publicacion
        #recortar imagen
        cropped_image_data = self.request.POST.get('cropped_image')
        if cropped_image_data:
            try:
                format, imgstr = cropped_image_data.split(';base64,')
                ext = format.split('/')[-1] 
                file_name = f"{uuid.uuid4()}.{ext}"
                file = ContentFile(base64.b64decode(imgstr), name=file_name)
                form.instance.image = file
            except Exception as e:
                print("Error al procesar la imagen recortada:", e)
        return super().form_valid(form)



#EDITAR: Que edite el titulo y la descripcion
class PublicacionEditar(LoginRequiredMixin, UpdateView):
    model=Post
    template_name='aposts/post_form.html'
    success_url=reverse_lazy("publicacion_list")
    fields=["title", "body", "image"]
    #recortar imagen
    def form_valid(self, form):
        cropped_image_data = self.request.POST.get('cropped_image')
        if cropped_image_data:
            try:
                format, imgstr = cropped_image_data.split(';base64,')
                ext = format.split('/')[-1]
                file_name = f"{uuid.uuid4()}.{ext}"
                file = ContentFile(base64.b64decode(imgstr), name=file_name)
                form.instance.image = file
            except Exception as e:
                print("Error al procesar la imagen recortada en edición:", e)
        return super().form_valid(form)



# Vista para listar todas las publicaciones
class PublicacionListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'aposts/posts_list.html'
    context_object_name='posts'



#detalle publicacion, mostrar el puntaje y comentarios, guardar puntaje asociando la publicacion/user y guardar comentario asociando la publicacion/user
class PublicacionDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'aposts/post_detail.html'
    context_object_name = 'post'  # Nombre con el que se accede a la publicación en la plantilla

    # MOSTRAR PUNTAJE Y COMENTARIOS GUARDADOS
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object() #post que se esta viendo
        user = self.request.user #usuario actual        
        scores = post.puntajes_posteo.all() # Obtener todos los puntajes 
        total_scores = scores.aggregate(total=Sum('score'))['total'] or 0
        score_distribution = {  # Contar por cada valor (1-5)
            1: scores.filter(score=1).count(),
            2: scores.filter(score=2).count(),
            3: scores.filter(score=3).count(),
            4: scores.filter(score=4).count(),
            5: scores.filter(score=5).count()}
        context['scores'] = scores
        context['total_scores'] = total_scores
        context['score_distribution'] = score_distribution
        context['author'] = post.user
        context['comments'] = post.comentarios.all()
        context['comment_form'] = CommentForm()
        score = post.puntajes_posteo.filter(user=user).first()
        context['score_form'] = ScoreForm(instance=score) if score else ScoreForm()
        context['user_has_scored'] = post.puntajes_posteo.filter(user=self.request.user).exists()
        return context

    # GUARDAR PUNTAJE O COMENTARIO
    def post(self, request, * args, **kwargs):
        self.object = self.get_object()
        user = request.user
        post = self.object
        form_type = request.POST.get('form_type')
        if form_type == 'comentario':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = user
                comment.post = post
                comment.save()
        elif form_type == 'puntaje':
            score = post.puntajes_posteo.filter(user=user).first()
            form = ScoreForm(request.POST, instance=score)
            if form.is_valid():
                score = form.save(commit=False)
                score.user = user
                score.post = post
                score.save()
        return redirect('publicacion_detail', pk=post.pk)


#eliminar publicacion
class PublicacionEliminar(LoginRequiredMixin, DeleteView):
    model=Post
    success_url=reverse_lazy('publicacion_list')