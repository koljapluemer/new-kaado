from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import CardListView, CardCreateView, CardUpdateView, CardDeleteView

urlpatterns = [
    path('', views.queue, name='queue'),
    # admin
    path('admin/', admin.site.urls),
    # stats
    path('stats', views.stats),
    # cards pregenerated
    path('cards', CardListView.as_view(), name='card_list'),
    path('cards/new', CardCreateView.as_view(), name='card_new'),
    path('cards/<int:pk>/update', CardUpdateView.as_view(), name='card_update'),
]
