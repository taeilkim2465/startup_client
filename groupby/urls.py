from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'groupby'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:startup_id>/', views.detail, name='detail'),
    path('startup/upload/', views.startup_upload, name='startup_upload'),
    path('startup/upload/create/', views.startup_upload_create, name='startup_upload_create'),
    path('startup/upload/update/<int:startup_id>/', views.startup_upload_update, name='startup_upload_update'),
    path('startup/upload/update/create/<int:startup_id>/', views.startup_upload_update_create, name='startup_upload_update_create'),
    path('startup/upload/delete/<int:startup_id>/', views.startup_upload_delete, name='startup_upload_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
