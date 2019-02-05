from django.urls import path
from . import views


urlpatterns = [
    path('', views.clients_list, name='client_list'),
    path('<int:client_id>', views.client_card, name='client_card'),
    path('create', views.client_create, name='client_create'),
    path('delete', views.client_delete, name='client_delete'),
    path('download', views.data_to_xlsx, name='data_to_xlsx'),
    path('photo', views.client_photo, name='client_photo'),
    path('api/photo/', views.ClientPhotoViewSet.as_view(), name='api_photo_list'),
    path('api/like', views.LikeClientPhotoView.as_view(), name='api_like'),
    path('api/login', views.login, name='login'),
]
