from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('', views.ClientsList.as_view(), name='client_list'),
    path('<int:pk>', views.ClientCard.as_view(), name='client_card'),
    path('create', views.ClientCreate.as_view(), name='client_create'),
    path('<int:pk>/delete/', views.ClientDelete.as_view(), name='client_delete'),
    path('deleted/', TemplateView.as_view(template_name="clientbase/client_deleted.html"), name='client_deleted'),
    path('download', views.data_to_xlsx, name='data_to_xlsx'),
    path('photo', views.ClientPhotoList.as_view(), name='client_photo'),
    path('api/photo/', views.ClientPhotoViewSet.as_view(), name='api_photo_list'),
    path('api/like', views.LikeClientPhotoView.as_view(), name='api_like'),
    path('api/login', views.LoginView.as_view(), name='api_login'),
]
