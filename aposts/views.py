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


#serch
@login_required
def searchProfiles(request):
    query = request.GET.get('q', '').strip()
    resultados = []    
    if query: 
        resultados = (Profile.objects.filter(Q(user__username__icontains=query)).select_related('user').annotate(total_posts=Count('user__posteo'), 
                    start=Case(When(user__username__istartswith=query, then=1), default=0, output_field=IntegerField())).order_by('-start', '-total_posts'))[:12]
    context = {'resultados': resultados, 'query': query}        
    return render(request, "aposts/search.html", context)

#delete comment
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user:
        return redirect('publicacion_detail', pk=comment.post.pk)  
    post_pk = comment.post.pk
    comment.delete()
    return redirect('publicacion_detail', pk=post_pk)  








# create without score
class PublicacionCrear(LoginRequiredMixin, CreateView):
    model=Post
    template_name='aposts/post_form.html'
    success_url=reverse_lazy('publicacion_list')
    fields=['title','body', 'image']    
    # add user and cut image
    def form_valid(self, form):
        form.instance.user=self.request.user
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



#Edit title and description
class PublicacionEditar(LoginRequiredMixin, UpdateView):
    model=Post
    template_name='aposts/post_form.html'
    success_url=reverse_lazy("publicacion_list")
    fields=["title", "body", "image"]
    #cut image
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




class PublicacionListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'aposts/posts_list.html'
    context_object_name='posts'



# publication detail, show qualifs and comments
class PublicacionDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'aposts/post_detail.html'
    context_object_name = 'post'

    # consultScoreComment() Read
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object() #this post
        user = self.request.user       
        scores = post.puntajes_posteo.all() # all scores 
        total_scores = scores.aggregate(total=Sum('score'))['total'] or 0
        score_distribution = {  
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

    # saveScoreCommet() Create / Update
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



class PublicacionEliminar(LoginRequiredMixin, DeleteView):
    model=Post
    success_url=reverse_lazy('publicacion_list')