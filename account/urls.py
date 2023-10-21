from django.urls import path
from .views import create_account,account_list,delete_account ,edit_account ,login_view,update_account,transaction

urlpatterns = [
    path('create_account/', create_account, name='create_account'),
    path('account_list/', account_list, name='account_list'),
    path('delete_account/<int:account_id>/', delete_account, name='delete_account'),
    path('update_account/<int:id>/', update_account, name='update_account'),
    path('login/', login_view, name='login'),
    path('edit_account/', edit_account, name='edit_account'),
    path('transaction/<int:id>/',transaction, name='transaction'),

]
