from django.urls import path
from . import views


urlpatterns = [
    path('', views.clients_list, name='client_list'),
    path('<int:client_id>', views.client_card, name='client_card'),
    path('create', views.client_create, name='client_create'),
    path('delete/<int:client_id>', views.client_delete, name='client_delete'),
]
