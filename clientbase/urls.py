"""
Module contain clientbase urls
"""

from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('', views.ClientsList.as_view(), name='client_list'),
    path('<int:pk>', views.ClientCard.as_view(), name='client_card'),
    path('create', views.ClientCreate.as_view(), name='client_create'),
    path('<int:pk>/delete/', views.ClientDelete.as_view(),
         name='client_delete'),
    path('deleted/',
         TemplateView.as_view(template_name="clientbase/client_deleted.html"),
         name='client_deleted'),
    path('download', views.data_to_xlsx, name='data_to_xlsx'),
    path('photo', views.ClientPhotoList.as_view(), name='client_photo'),
    path('like', views.LikeClientPhotoView.as_view(), name='like_photo'),
    path('like_async',
         views.LikeClientPhotoAsyncView.as_view(),
         name='like_photo_async'
         ),
]
