# wallet_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    END_USER = 'end_user'
    OWNER = 'owner'
    ROLE_CHOICES = [
        (END_USER, 'End User'),
        (OWNER, 'Owner'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=END_USER)


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    linked_bank_account = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"
    


@receiver(post_save, sender=Transaction)
def perform_wallet_transaction(sender, instance, created, **kwargs):
    if created:
        end_user = instance.user
        amount = instance.amount

        end_user_wallet = Wallet.objects.get(user=end_user)
        owner_wallet = Wallet.objects.filter(user__role=User.OWNER).first()

        end_user_wallet.balance -= amount
        owner_wallet.balance += amount

        end_user_wallet.save()
        owner_wallet.save()

        total_addition = Wallet.objects.aggregate(Sum('balance'))['balance__sum']
        total_deduction = -total_addition
        print(f"Total Addition: {total_addition}")
        print(f"Total Deduction: {total_deduction}")
        


@receiver(post_save, sender=Transaction)
def perform_wallet_transaction(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        amount = instance.amount

        user_wallet = Wallet.objects.get(user=user)
        if user.role == User.END_USER:
            user_wallet.balance -= amount
        elif user.role == User.OWNER:
            user_wallet.balance -= amount
            user_wallet.linked_bank_account += amount  # Simulated transfer to linked bank account

        user_wallet.save()

        total_addition = Wallet.objects.aggregate(Sum('balance'))['balance__sum']
        total_deduction = -total_addition
        print(f"Total Addition: {total_addition}")
        print(f"Total Deduction: {total_deduction}")