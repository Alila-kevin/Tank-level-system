from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('view/', views.view_data, name='view_data'),
]
