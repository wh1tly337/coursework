from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog', views.catalog, name='catalog'),
    path('about_us', views.about_us, name='about_us'),
    path('chect_out', views.chect_out, name='chect_out'),
    path('comming_soon', views.comming_soon, name='comming_soon'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('product_id=<int:pk>', views.product_card, name='product_card'),
    path('cart', views.cart, name='cart'),
    path('refound', views.refound, name='refound'),
    path('purchase', views.purchase, name='purchase'),
    path('appeal', views.appeal, name='appeal'),
    path('entrance', views.entrance, name='entrance'),
    path('registration', views.registration, name='registration'),
    path('logout', views.logout, name='logout'),
    path('account_deleting', views.account_deleting, name='account_deleting')
]
