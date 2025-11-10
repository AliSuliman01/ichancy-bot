from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    telegram_id = models.CharField(max_length=25, unique=True)
    telegram_username = models.CharField(max_length=255, blank=True, null=True)
    player_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    referal_code = models.CharField(max_length=255, unique=True)
    referal_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    balance = models.IntegerField(default=0)
    account_balance = models.IntegerField(default=0)

    class Meta:
        db_table = 'users'
        managed = False

class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    provider_id = models.IntegerField(blank=True, null=True)
    provider_type = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    value = models.IntegerField()
    action_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transactions'
        managed = False

class AccountTransactions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    status = models.CharField(max_length=255)
    action_type = models.CharField(max_length=255)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'account_transactions'
        managed = False

class BemoTransactions(models.Model):
    id = models.AutoField(primary_key=True)
    transfeer_num = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    status = models.CharField(max_length=255)
    action_type = models.CharField(max_length=255)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bemo_transactions'
        managed = False

class SyriatelTransactions(models.Model):
    id = models.AutoField(primary_key=True)
    transfeer_num = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    status = models.CharField(max_length=255)
    action_type = models.CharField(max_length=255)
    value = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'syriatel_transactions'
        managed = False

class ShamCashTransactions(models.Model):
    id = models.AutoField(primary_key=True)
    transfeer_num = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    status = models.CharField(max_length=255)
    action_type = models.CharField(max_length=255)
    value = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sham_cash_transactions'
        managed = False

class OrderMoneyTransactions(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    city_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    status = models.CharField(max_length=255)
    action_type = models.CharField(max_length=255)
    value = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_money_transactions'
        managed = False

class CryptoTransactions(models.Model):
    id = models.AutoField(primary_key=True)
    transfeer_num = models.CharField(max_length=255, blank=True, null=True)
    currency_name = models.CharField(max_length=50, blank=True, null=True)
    network_name = models.CharField(max_length=50, blank=True, null=True)
    SYP_for_unit = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    status = models.CharField(max_length=255)
    action_type = models.CharField(max_length=255)
    value = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'crypto_transactions'
        managed = False

class Gifts(models.Model):
    id = models.AutoField(primary_key=True)
    telegram_goal_id = models.CharField(max_length=20)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    redeemed_at = models.DateTimeField(blank=True, null=True)
    code = models.CharField(max_length=25)
    ammount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gifts'
        managed = False

class MessagesToAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    message = models.TextField()
    photo = models.TextField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages_to_admin'
        managed = False