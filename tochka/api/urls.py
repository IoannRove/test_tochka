from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path(
        'account_list/', views.AccountViewSet.as_view({'get': 'list'}),
        name='account_list'
    ),
    path(
        'ping/', views.ping,
        name='ping'
    ),
    path(
        'status/<uuid:pk>', views.AccountViewSet.as_view({'get': 'retrieve'}),
        name='status'
    ),
    path(
        'add/<uuid:pk>', views.AddSumToBalanceViewSet.as_view({'post': 'update'}),
        name='add'
    ),
    path(
        'subtract/<uuid:pk>', views.SubtractBalanceViewSet.as_view({'post': 'update'}),
        name='subtract'
    ),
])
