from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import BankAccount
from django.contrib import messages
from django.contrib.auth import authenticate, login
from decimal import Decimal
def create_account(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        balance = request.POST['balance']
        account_number = request.POST['account_number']

        # Check if passwords match
        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('create_account')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('create_account')

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.save()

        # Create a bank account for the user
        BankAccount.objects.create(account_number=account_number, user=user, balance=balance)

        # Log in the user
        user = authenticate(request, username=username, password=password)
        login(request, user)

        messages.success(request, 'Account created successfully!')
        return redirect('create_account')

    return render(request, 'account/create_account.html')


def account_list(request):
    accounts = BankAccount.objects.select_related('user').all()
    return render(request, 'account/account_list.html', {'accounts': accounts})

def delete_account(request, account_id):
    result=BankAccount.objects.get(pk=account_id)
    result.delete()
    return redirect('/account/account_list/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/account/account_list/') 
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'account/login.html')

def edit_account(request):
    # area=Area.objects.all()
    id = request.user.id
    result=  BankAccount.objects.get(user_id=id)
    result1=  User.objects.get(pk=id)
    context={'result':result, 'result1':result1}
    return render(request,'account/edit_account.html',context)

def update_account(request,id):
    fname     = request.POST['fname']
    lname     = request.POST['lname']
    email     = request.POST['email']
  

    user=User.objects.update_or_create(pk=request.user.id, defaults={'first_name':fname,'last_name':lname,'email':email})
    return redirect('/account/login/')


def transaction(request, id):
    account = get_object_or_404(BankAccount, pk=id)

    if request.method == 'POST':
        action = request.POST['action']
        amount = float(request.POST['amount'])

        if action == 'deposit':
            account.balance += amount
        elif action == 'withdraw':
            if amount <= account.balance:
                account.balance -= amount
            else:
                messages.error(request, 'Insufficient balance for withdrawal.')
                return redirect('transaction', id=id)

        account.save()
        messages.success(request, f'Funds {action}ed successfully!')
        return redirect('transaction', id=id)

    return render(request, 'account/edit_account.html', {'account': account})


def transaction(request, id):
    account = get_object_or_404(BankAccount, pk=id)

    if request.method == 'POST':
        action = request.POST['action']
        amount_str = request.POST['amount']

        try:
            amount = Decimal(amount_str)
        except ValueError:
            messages.error(request, 'Invalid amount format.')
            return redirect('transaction', id=id)

        if action == 'deposit':
            account.balance += amount
        elif action == 'withdraw':
            if amount <= account.balance:
                account.balance -= amount
            else:
                messages.error(request, 'Insufficient balance for withdrawal.')
                return redirect('transaction', id=id)

        account.save()
        messages.success(request, f'Funds {action}ed successfully!')
        return redirect('transaction', id=id)

    return render(request, 'account/edit_account.html', {'account': account})
