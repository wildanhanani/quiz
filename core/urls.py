from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('healthz/', views.healthz, name='healthz'),
    path('offline/', views.offline, name='offline'),
    path('pricing/', views.pricing, name='pricing'),
    path('register/', views.register, name='register'),
]
