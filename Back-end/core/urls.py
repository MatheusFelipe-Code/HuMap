from django.urls import path
from .views import (
    DenunciaListCreateView,
    home_view,
    suporte_view,
    configuracao_view,
    tutorial_view,
    feed_view,
    sobre_view
)

app_name = 'core'

urlpatterns = [
    path('home/', home_view, name='home'),
    path('suporte/', suporte_view, name='suporte'),
    path('configuracao/', configuracao_view, name='configuracao'),
    path('tutorial/', tutorial_view, name='tutorial'),
    path('feed/', feed_view, name='feed'),

    path('api/denuncias/', DenunciaListCreateView.as_view(), name='lista-denuncias'),
]
