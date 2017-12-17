from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^book/$', views.book, name='book'),
    url(r'^current/$', views.current, name='current'),

]