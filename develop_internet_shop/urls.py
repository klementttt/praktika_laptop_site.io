from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from products.views import (
    home, information_view, where_to_find_us_view, catalog_view, 
    login_view, logout_view, success_view, register_view, cart_view, 
    add_to_cart_view, remove_from_cart_view, product_detail_view  # Добавляем import remove_from_cart_view
)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls), 
    path('information/', information_view, name='information'),
    path('where_to_find_us/', where_to_find_us_view, name='where_to_find_us'),
    path('catalog/', catalog_view, name='catalog'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart_view, name='remove_from_cart'),  # Новый маршрут для удаления товаров из корзины
    path('product/<int:pk>/', product_detail_view, name='product_detail'),  # Новый маршрут для детальной страницы продукта
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
