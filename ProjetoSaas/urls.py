from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Inclui as URLs da aplicação "core"
    path('accounts/', include('django.contrib.auth.urls')),  # URLs de autenticação padrão do Django
]