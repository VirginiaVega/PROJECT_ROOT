# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from aposts.models import Post, Score
from .forms import ScoreForm, CommentForm
from django.shortcuts import redirect


#Crea sin agregar el puntaje, pero si agregando el usuario
class PublicacionCrear(LoginRequiredMixin, CreateView):
    model=Post
    template_name='aposts/post_form.html'
    success_url=reverse_lazy('publicacion_list')
    fields=['title','body']    

    #Asigna el usuario
    def form_valid(self, form):
        form.instance.user=self.request.user #Toma el usuario para guarar la publicacion
        return super().form_valid(form)

#EDITAR: Que edite el titulo y la descripcion
class PublicacionEditar(LoginRequiredMixin, UpdateView):
    model=Post
    template_name='aposts/post_form.html'
    success_url=reverse_lazy("publicacion_list")
    fields=["title", "body"]

# Vista para listar todas las publicaciones, y el numero total de ellas
class PublicacionListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'aposts/posts_list.html'
    context_object_name='posts'
    
    #LISTAR TOTAL DE PUBLICACIONES
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['post_count'] = Post.objects.count()
        return context #devuelve el contexto


#detalle publicacion, mostrar el puntaje y comentarios, guardar puntaje asociando la publicacion/user y guardar comentario asociando la publicacion/user
class PublicacionDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'aposts/post_detail.html'
    context_object_name = 'post'  # Nombre con el que se accede a la publicación en la plantilla

    # MOSTRAR PUNTAJE Y COMENTARIOS GUARDADOS
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        user = self.request.user
        context['scores'] = post.puntajes_posteo.all()
        context['author'] = post.user
        context['comments'] = post.comentarios.all()
        context['comment_form'] = CommentForm()
        score = post.puntajes_posteo.filter(user=user).first()
        context['score_form'] = ScoreForm(instance=score) if score else ScoreForm()
        return context

    # GUARDAR PUNTAJE O COMENTARIO
    def post(self, request, *args, **kwargs):
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