"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#for render star
from django.http import HttpResponse
from django.core.management import execute_from_command_line
import os

def run_migrations_view(request):
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        return HttpResponse('✅ Migraciones ejecutadas exitosamente. Ahora puedes acceder a /admin/')
    except Exception as e:
        return HttpResponse(f'❌ Error: {str(e)}')
#for render end



urlpatterns = [
    path('admin/', admin.site.urls),
    path('run-migrations/', run_migrations_view),  # ← URL TEMPORAL render
    path('', include('accounts.urls')),
    path('post/', include('aposts.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
