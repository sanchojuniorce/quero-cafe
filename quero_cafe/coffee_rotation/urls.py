from django.conf.urls import url
from coffee_rotation import views

urlpatterns = [
    url(r'^list', views.list, name='list'),
    url(r'^set-as-voluntary', views.set_as_voluntary, name='set_as_voluntary'),
    url(r'^choose-randomly', views.choose_randomly, name='choose_randomly'),
    url(r'^remove-from-turn/(?P<id>(\d+))', views.remove_turn, name='remove_turn'),
]