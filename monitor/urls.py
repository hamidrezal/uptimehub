from django.urls import path
from monitor import views

app_name = 'monitor'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('api/check/', views.ServerStatusAPIView.as_view(), name='api_check'),
    path('servers/', views.ServerListView.as_view(), name='server_list'),
    path('servers/create/', views.ServerCreateView.as_view(), name='server_create'),
    path('servers/<int:pk>/update/', views.ServerUpdateView.as_view(), name='server_update'),
    path('servers/<int:pk>/delete/', views.ServerDeleteView.as_view(), name='server_delete'),
    path('servers/<int:pk>/check/', views.ServerCheckView.as_view(), name='server_check'),
    path('servers/<int:pk>/toggle/', views.ServerToggleView.as_view(), name='server_toggle'),
]