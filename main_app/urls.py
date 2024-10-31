from django.urls import path
from . import views

urlpatterns = [
    path('cats/', views.cat_index, name='cat-index'),
    path('accounts/signup/', views.signup, name='signup'),

    path('cats/<int:cat_id>/', views.cat_detail, name='cat-detail'),
    path('cats/create/', views.CatCreate.as_view(), name='cat-create'),
    path('cats/<int:pk>/update/', views.CatUpdate.as_view(), name='cat-update'),
    path('cats/<int:pk>/delete/', views.CatDelete.as_view(), name='cat-delete'),
    path('cats/<int:cat_id>/give-toy/<int:toy_id>/', views.give_toy, name='give-toy'),
    path('cats/<int:cat_id>/remove-toy/<int:toy_id>/', views.remove_toy, name='remove-toy'),  # New path for removing a toy
    path('toys/', views.ToyList.as_view(), name='toy-index'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toy-detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toy-create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toy-update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toy-delete'),
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('cats/<int:cat_id>/add-feeding/', views.add_feeding, name='add-feeding'),
  
]


