"""
URL configuration for nitin_deploy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path('', home, name='home_page'),

    path(
        'category/<slug:slug>/',
        category_products,
        name='category_products'
    ),

    path(
        'add-to-cart/<int:product_id>/',
        add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        cart_view,
        name='cart'
    ),

    path(
        'increase-quantity/<int:product_id>/',
        increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease-quantity/<int:product_id>/',
        decreate_quantity,
        name='decrease_quantity'
    ),

    path(
        'remove-item/<int:product_id>/',
        remove_item,
        name='remove_item'
    ),

    path(
        'address/',
        address_page,
        name='address_page'
    ),

    path(
        'edit-address/<int:id>/',
        edit_address,
        name='edit_address'
    ),

    path(
        'checkout/',
        checkout,
        name='checkout'
    ),

    path(
        'order-success/<int:id>/',
        order_success,
        name='order_success'
    ),

    path(
        'my-orders/',
        my_orders,
        name='my_orders'
    ),

    path(
        'register/',
        register_form,
        name='register_page'
    ),

    path(
        'login/',
        login_form,
        name='login_page'
    ),

    path(
        'logout/',
        logout_page,
        name='logout_page'
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )



