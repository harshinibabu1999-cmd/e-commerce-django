from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myapp2'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('', views.home, name='home'),
    path('dashboard-login/', views.dashboard_login, name='dashboard_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout, name='logout'),
    path('admin/add-product/', views.admin_add_product, name='admin_add_product'),
    path('products/', views.product_list, name='product_list'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('customer-list/',views.customer_list,name='customer_list'),
    path('customer-product-list/',views.customer_product_list,name='customer_product_list'),
    path('wishlist/<int:product_id>/', views.wishlist, name='wishlist'),
    path('wishlist-view/',views.wishlist_view,name='wishlist_view'),
    path('buy-now/<int:product_id>/',views.buy_product,name='buy_product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-quantity/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('payment-successful/', views.payment_successful, name='payment_successful'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('product/<int:product_id>/', views.product_view, name='product_view'),
    path('orders/', views.order_list, name='order_list'),
    path('profile/', views.profile_view, name='profile_view'),
    path('my-orders/', views.my_orders, name='my_orders'),


]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
