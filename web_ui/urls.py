from django.urls import path
from web_ui import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('items/<int:category>', views.ItemsView.as_view(), name='items'),
    path('items/detail/<int:pk>', views.ItemsDetailView.as_view(), name='items-detail'),
    path('orders/', views.OrdersView.as_view(), name='orders-list'),
]
