from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    # pages
    path('', views.home, name='index'),
    path('accounts/reset/done/', views.home),
    path('about', views.about),
    path('premium', views.premium),
    path('settings', views.settings),
    path('privacy', views.privacy),
    path('terms', views.tos),
    # Users
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/changeEmail', views.changeEmail),
    # signup is direct, convert is for people who had a temporary acc
    path('convert', include('lazysignup.urls'), {'template_name': 'pages/signup.html'}),

    path('profile', views.profile),
    path('deleteUser', views.deleteUser),

    # new attempt to get stripe running
    path('success/', views.success),
    path('cancel/', views.cancel),

    # yet another attempt to stripe
    path('payment_form', views.payment_form),

    # admin
    path('admin/', admin.site.urls),
]
