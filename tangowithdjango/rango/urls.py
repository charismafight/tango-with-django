from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

app_name = 'rango'

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  url(r'^about/$', views.about, name='about'),
                  url(r'^category/(.*)$', views.category, name='category'),
                  url(r'^add_category/$', views.add_category, name='add_category'),
                  url(r'^category/(.*)/add_page/$', views.add_page, name='add_page'),
                  url(r'^login/$', views.user_login, name='login'),
                  url(r'^restrict/$', views.restrict, name='restrict'),
                  url(r'^user_logout/$', views.user_logout, name='user_logout'),
                  url(r'^goto/', views.track_url, name='goto'),
                  url(r'^like_category/$', views.like_category, name='like_category'),
                  url(r'^suggest_category/$', views.suggestion_category, name='suggest_category'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
