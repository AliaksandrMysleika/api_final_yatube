from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from api.urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
