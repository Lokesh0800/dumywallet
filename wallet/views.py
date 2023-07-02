# wallet_app/views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Wallet, Transaction
from .serializers import UserSerializer, WalletSerializer, TransactionSerializer


class UserDetailView(APIView):
    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class WalletDetailView(APIView):
    def get(self, request, format=None):
        user = request.user
        wallet = Wallet.objects.get(user=user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class TransactionListView(APIView):
    def get(self, request, format=None):
        user = request.user
        transactions = Transaction.objects.filter(user=user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
