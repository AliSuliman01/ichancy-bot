from django.contrib import admin
from .models import *

class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

@admin.register(Users)
class UsersAdmin(ReadOnlyAdmin):
    list_display = ['id', 'telegram_id', 'telegram_username', 'player_id', 'name', 'email', 'balance', 'created_at']
    list_filter = ['created_at']
    search_fields = ['telegram_id', 'telegram_username', 'name', 'email']
    list_per_page = 20

@admin.register(Transactions)
class TransactionsAdmin(ReadOnlyAdmin):
    list_display = ['id', 'user', 'provider_type', 'value', 'action_type', 'status', 'created_at']
    list_filter = ['action_type', 'status', 'created_at']
    search_fields = ['user__telegram_id', 'user__name']
    list_per_page = 20

@admin.register(AccountTransactions)
class AccountTransactionsAdmin(ReadOnlyAdmin):
    list_display = ['id', 'user', 'action_type', 'value', 'status', 'created_at']
    list_filter = ['action_type', 'status', 'created_at']
    search_fields = ['user__telegram_id', 'user__name']
    list_per_page = 20

@admin.register(BemoTransactions)
class BemoTransactionsAdmin(ReadOnlyAdmin):
    list_display = ['id', 'user', 'transfeer_num', 'action_type', 'value', 'status', 'created_at']
    list_filter = ['action_type', 'status', 'created_at']
    search_fields = ['user__telegram_id', 'transfeer_num']
    list_per_page = 20

@admin.register(SyriatelTransactions)
class SyriatelTransactionsAdmin(ReadOnlyAdmin):
    list_display = ['id', 'user', 'transfeer_num', 'action_type', 'value', 'status', 'created_at']
    list_filter = ['action_type', 'status', 'created_at']
    search_fields = ['user__telegram_id', 'transfeer_num']
    list_per_page = 20

@admin.register(ShamCashTransactions)
class ShamCashTransactionsAdmin(ReadOnlyAdmin):
    list_display = ['id', 'user', 'transfeer_num', 'action_type', 'value', 'status', 'created_at']
    list_filter = ['action_type', 'status', 'created_at']
    search_fields = ['user__telegram_id', 'transfeer_num']
    list_per_page = 20

@admin.register(OrderMoneyTransactions)
class OrderMoneyTransactionsAdmin(ReadOnlyAdmin):
    list_display = ['id', 'user', 'company_name', 'name', 'action_type', 'value', 'status', 'created_at']
    list_filter = ['action_type', 'status', 'company_name', 'created_at']
    search_fields = ['user__telegram_id', 'name', 'company_name']
    list_per_page = 20

@admin.register(CryptoTransactions)
class CryptoTransactionsAdmin(ReadOnlyAdmin):
    list_display = ['id', 'user', 'currency_name', 'network_name', 'action_type', 'value', 'status', 'created_at']
    list_filter = ['action_type', 'status', 'currency_name', 'created_at']
    search_fields = ['user__telegram_id', 'currency_name', 'transfeer_num']
    list_per_page = 20

@admin.register(Gifts)
class GiftsAdmin(ReadOnlyAdmin):
    list_display = ['id', 'user', 'telegram_goal_id', 'code', 'ammount', 'redeemed_at', 'created_at']
    list_filter = ['redeemed_at', 'created_at']
    search_fields = ['user__telegram_id', 'code', 'telegram_goal_id']
    list_per_page = 20

@admin.register(MessagesToAdmin)
class MessagesToAdminAdmin(ReadOnlyAdmin):
    list_display = ['id', 'user', 'message', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__telegram_id', 'message']
    list_per_page = 20