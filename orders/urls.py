from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.order_list, name='order_list'),
    path('order-details/<int:order_id>/', views.order_detail, name='order_detail'),
    path('adm/approve/<int:order_id>/', views.admin_approve_order, name='admin_approve_order'),
]
