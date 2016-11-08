from django.conf.urls import include, url
from django.contrib import admin

from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # COLABORADORES
    url(r'^', include('coffee_rotation.urls', namespace='')),

    # HOME
    url(r'^', RedirectView.as_view(url=reverse_lazy('list'))),
]