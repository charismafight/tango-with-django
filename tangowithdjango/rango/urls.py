from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

app_name = 'rango'

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  url(r'^about/$', views.about, name='about'),
                  url(r'^category/(\w*)$', views.category, name='category')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
