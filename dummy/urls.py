# wallet_project/urls.py
from django.contrib import admin

from django.urls import path
from wallet.views import UserDetailView, WalletDetailView, TransactionListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', UserDetailView.as_view(), name='user-detail'),
    path('api/wallet/', WalletDetailView.as_view(), name='wallet-detail'),
    path('api/transactions/', TransactionListView.as_view(), name='transaction-list'),
]
