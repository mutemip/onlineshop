from django.contrib import admin
from django.urls import path, include

import shop.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', shop.views.customerlogin, name='login'),
    path('accounts/logout/', shop.views.customerLogout, name='logout'),
    path('accounts/register/', shop.views.customerregister, name='register'),
    path('search/', shop.views.product_search, name='search'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('', include('shop.urls', namespace='shop')),
    path('', shop.views.product_list, name='product_list'),


]

admin.site.site_header = 'E-Com Trial'
admin.site.site_title = ''
admin.site.index_title = 'E-Com Trial'
