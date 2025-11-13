from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.group_list, name='list'),
    path('create/', views.group_create, name='create'),
    path('<int:pk>/', views.group_detail, name='detail'),
    path('<int:pk>/request/', views.group_request_join, name='request_join'),
    path('requests/', views.join_requests_list, name='requests'),
    path('requests/<int:membership_id>/approve/', views.approve_request, name='approve_request'),
    path('requests/<int:membership_id>/reject/', views.reject_request, name='reject_request'),
]
