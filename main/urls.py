from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    # pages
    path('', views.queue, name='queue'),
    path('accounts/reset/done/', views.home),
    # Users
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/changeEmail', views.changeEmail),

    path('profile', views.profile),
    path('deleteUser', views.deleteUser),

    # admin
    path('admin/', admin.site.urls),

    # stats
    path('stats', views.stats),
]
