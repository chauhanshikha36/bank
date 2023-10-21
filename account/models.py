from django.db import models
from django.db import models
from django.contrib.auth.models import User

class BankAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    