from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('account_list/', views.AccountViewSet.as_view({'get': 'list'})),
    path('status/<uuid:pk>', views.AccountViewSet.as_view({'get': 'retrieve'})),
    path('add/<uuid:pk>', views.AddSumToBalanceViewSet.as_view({'post': 'update'})),
    # path('subtract/<uuid:pk>', views.ChangeBalanceViewSet.as_view({'post': 'subtract'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
