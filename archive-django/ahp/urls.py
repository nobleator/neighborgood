from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^welcome', views.welcome, name='welcome'),
    url(r'^criteria', views.criteria, name='criteria'),
    url(r'^weights', views.weights, name='weights'),
    url(r'^results', views.results, name='results'),
]
