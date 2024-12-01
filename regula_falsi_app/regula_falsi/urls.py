# regula_falsi/urls.py
from django.urls import path
from .views import index

# Mendefinisikan URL yang tersedia untuk aplikasi regula_falsi
urlpatterns = [
    path('', index, name='index'),  # Mengarahkan root URL ('/') ke fungsi view 'index'
]
