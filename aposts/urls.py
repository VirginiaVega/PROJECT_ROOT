from django.urls import path
from aposts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('new/',views.PublicacionCrear.as_view(),name='publicacion_crear'),
    path('list/', views.PublicacionListView.as_view(), name='publicacion_list'), 
    path('detail/<int:pk>',views.PublicacionDetailView.as_view(), name='publicacion_detail'),
    path('edit/<int:pk>', views.PublicacionEditar.as_view(),name='publicacion_editar'),
    path('delete/<int:pk>', views.PublicacionEliminar.as_view(),name='publicacion_eliminar'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('search/',views.searchProfiles, name='search'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)