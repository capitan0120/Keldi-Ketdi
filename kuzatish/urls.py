from django.urls import path
from .views import xodimlar_list, xodim_detail, index, period_view, haftalik_view, oylik_view, create_view, \
    xodimlar_ruyxati, haftalik_tarix, oylik_malumotlar

urlpatterns = [
    path('xodimlar/', xodimlar_list, name='xodimlar-list'),
    path('xodimlar/<int:pk>/', xodim_detail, name='xodim-detail'),
    path('index/', index, name='index'),
    path('period/', period_view, name='period'),
    path('haftalik/', haftalik_view, name='haftalik'),
    path('haftalik_tarix/<int:pk>/', haftalik_tarix, name='haftalik-tarix'),
    path('oylik/', oylik_view, name='oylik'),
    path('create/', create_view, name='create-xodim'),
    path('xodimlar_ruyxati/', xodimlar_ruyxati, name='xodimlar-ruyxati'),
    path('example/', oylik_malumotlar, name='example'),
]





# path('register/', register, name='register'),
# path('otp/', otp_view, name='otp')