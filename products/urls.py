from django.urls import path,include
from products.views import *
urlpatterns = [
    path('',products_lst,name='products-list'),
    path('products/',products_lst,name='products_list'),

]
