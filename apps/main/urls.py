from django.urls import path
from apps.main import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'


urlpatterns = [
    path('', views.MainPageView.as_view(), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
