from django.urls import path
from aposts import views

urlpatterns = [
    path('new/',views.PublicacionCrear.as_view(),name='publicacion_crear'),
    path('list/', views.PublicacionListView.as_view(), name='publicacion_list'), 
    path('detail/<int:pk>',views.PublicacionDetailView.as_view(), name='publicacion_detail'),
    path('edit/<int:pk>', views.PublicacionEditar.as_view(),name='publicacion_editar'),
    path('delete/<int:pk>', views.PublicacionEliminar.as_view(),name='publicacion_eliminar'),
]