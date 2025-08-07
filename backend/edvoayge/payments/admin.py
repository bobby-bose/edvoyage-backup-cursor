from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count, Q
from django.utils import timezone
from .models import (
    PaymentMethod,
    PaymentTransaction,
    Subscription,
    Invoice,
    Refund,
    PaymentGateway,
    PaymentLog,
)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'payment_type', 'name', 'is_default', 'is_active',
        'card_last4', 'card_brand', 'bank_name', 'created_at'
    ]
    list_filter = [
        'payment_type', 'is_default', 'is_active', 'created_at',
        'user__email'
    ]
    search_fields = [
        'name', 'user__email', 'user__first_name', 'user__last_name',
        'card_last4', 'bank_name'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at'
    ]
    list_select_related = ['user']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'payment_type', 'name', 'is_default', 'is_active')
        }),
        ('Card Information', {
            'fields': ('card_last4', 'card_brand', 'card_exp_month', 'card_exp_year'),
            'classes': ('collapse',)
        }),
        ('Bank Information', {
            'fields': ('bank_name', 'account_last4', 'account_type'),
            'classes': ('collapse',)
        }),
        ('Digital Wallet', {
            'fields': ('wallet_type', 'wallet_id'),
            'classes': ('collapse',)
        }),
        ('Security', {
            'fields': ('encrypted_data', 'token'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_methods', 'deactivate_methods', 'set_as_default']
    
    def activate_methods(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} payment methods activated.')
    activate_methods.short_description = "Activate selected payment methods"
    
    def deactivate_methods(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} payment methods deactivated.')
    deactivate_methods.short_description = "Deactivate selected payment methods"
    
    def set_as_default(self, request, queryset):
        for method in queryset:
            # Remove default from other methods of the same user
            PaymentMethod.objects.filter(
                user=method.user, is_default=True
            ).exclude(id=method.id).update(is_default=False)
            method.is_default = True
            method.save()
        self.message_user(request, f'{queryset.count()} payment methods set as default.')
    set_as_default.short_description = "Set selected payment methods as default"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id', 'user', 'transaction_type', 'amount', 'currency',
        'status', 'gateway', 'created_at', 'is_successful'
    ]
    list_filter = [
        'transaction_type', 'status', 'currency', 'gateway', 'created_at',
        'user__email'
    ]
    search_fields = [
        'transaction_id', 'description', 'user__email', 'user__first_name',
        'user__last_name', 'gateway_transaction_id'
    ]
    readonly_fields = [
        'id', 'transaction_id', 'created_at', 'updated_at', 'processed_at',
        'completed_at', 'is_successful', 'is_refundable'
    ]
    list_select_related = ['user', 'payment_method']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'transaction_id', 'user', 'payment_method')
        }),
        ('Transaction Details', {
            'fields': ('transaction_type', 'amount', 'currency', 'status', 'description')
        }),
        ('Related Objects', {
            'fields': ('related_object_type', 'related_object_id'),
            'classes': ('collapse',)
        }),
        ('Payment Processing', {
            'fields': ('gateway', 'gateway_transaction_id', 'gateway_response'),
            'classes': ('collapse',)
        }),
        ('Fees and Taxes', {
            'fields': ('processing_fee', 'tax_amount', 'discount_amount'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'processed_at', 'completed_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_failed', 'mark_as_cancelled']
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(
            status='completed',
            processed_at=timezone.now(),
            completed_at=timezone.now()
        )
        self.message_user(request, f'{updated} transactions marked as completed.')
    mark_as_completed.short_description = "Mark selected transactions as completed"
    
    def mark_as_failed(self, request, queryset):
        updated = queryset.update(status='failed')
        self.message_user(request, f'{updated} transactions marked as failed.')
    mark_as_failed.short_description = "Mark selected transactions as failed"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} transactions marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected transactions as cancelled"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'payment_method')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'plan_name', 'subscription_type', 'status', 'amount',
        'currency', 'is_active', 'days_remaining', 'created_at'
    ]
    list_filter = [
        'subscription_type', 'status', 'currency', 'auto_renew', 'created_at',
        'user__email'
    ]
    search_fields = [
        'plan_name', 'description', 'user__email', 'user__first_name',
        'user__last_name'
    ]
    readonly_fields = [
        'id', 'is_active', 'is_trial', 'days_remaining', 'created_at', 'updated_at'
    ]
    list_select_related = ['user', 'payment_method']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'plan_name', 'subscription_type', 'status')
        }),
        ('Billing Details', {
            'fields': ('amount', 'currency', 'billing_cycle', 'payment_method')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'trial_end_date', 'cancelled_at')
        }),
        ('Auto-renewal', {
            'fields': ('auto_renew', 'next_billing_date'),
            'classes': ('collapse',)
        }),
        ('Features and Limits', {
            'fields': ('features', 'limits'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('description', 'metadata'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_subscriptions', 'cancel_subscriptions', 'extend_trial']
    
    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} subscriptions activated.')
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def cancel_subscriptions(self, request, queryset):
        updated = queryset.update(
            status='cancelled',
            cancelled_at=timezone.now(),
            auto_renew=False
        )
        self.message_user(request, f'{updated} subscriptions cancelled.')
    cancel_subscriptions.short_description = "Cancel selected subscriptions"
    
    def extend_trial(self, request, queryset):
        from datetime import timedelta
        for subscription in queryset:
            if subscription.trial_end_date:
                subscription.trial_end_date += timedelta(days=7)
                subscription.save()
        self.message_user(request, f'{queryset.count()} trial periods extended by 7 days.')
    extend_trial.short_description = "Extend trial by 7 days"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'payment_method')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number', 'user', 'status', 'amount', 'currency',
        'due_date', 'is_overdue', 'days_overdue', 'created_at'
    ]
    list_filter = [
        'status', 'currency', 'created_at', 'due_date', 'user__email'
    ]
    search_fields = [
        'invoice_number', 'user__email', 'user__first_name', 'user__last_name',
        'notes'
    ]
    readonly_fields = [
        'id', 'invoice_number', 'is_overdue', 'days_overdue', 'created_at', 'updated_at'
    ]
    list_select_related = ['user', 'transaction', 'subscription']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'invoice_number', 'user', 'transaction', 'subscription')
        }),
        ('Invoice Details', {
            'fields': ('status', 'amount', 'currency')
        }),
        ('Billing Information', {
            'fields': ('billing_address', 'shipping_address'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('issue_date', 'due_date', 'paid_date')
        }),
        ('Items and Totals', {
            'fields': ('items', 'subtotal', 'tax_amount', 'discount_amount', 'total_amount'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes', 'terms_conditions'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_paid', 'mark_as_sent', 'mark_as_overdue']
    
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(
            status='paid',
            paid_date=timezone.now()
        )
        self.message_user(request, f'{updated} invoices marked as paid.')
    mark_as_paid.short_description = "Mark selected invoices as paid"
    
    def mark_as_sent(self, request, queryset):
        updated = queryset.update(status='sent')
        self.message_user(request, f'{updated} invoices marked as sent.')
    mark_as_sent.short_description = "Mark selected invoices as sent"
    
    def mark_as_overdue(self, request, queryset):
        updated = queryset.update(status='overdue')
        self.message_user(request, f'{updated} invoices marked as overdue.')
    mark_as_overdue.short_description = "Mark selected invoices as overdue"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'transaction', 'subscription')


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = [
        'refund_id', 'transaction', 'user', 'amount', 'currency', 'status',
        'reason', 'is_successful', 'created_at'
    ]
    list_filter = [
        'status', 'reason', 'currency', 'created_at', 'user__email'
    ]
    search_fields = [
        'refund_id', 'user__email', 'user__first_name', 'user__last_name',
        'notes', 'gateway_refund_id'
    ]
    readonly_fields = [
        'id', 'refund_id', 'is_successful', 'created_at', 'updated_at', 'processed_at'
    ]
    list_select_related = ['transaction', 'user']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'refund_id', 'transaction', 'user')
        }),
        ('Refund Details', {
            'fields': ('amount', 'currency', 'status', 'reason')
        }),
        ('Processing', {
            'fields': ('gateway_refund_id', 'gateway_response'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'processed_at'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['process_refunds', 'mark_as_completed', 'mark_as_failed']
    
    def process_refunds(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='processing'
        )
        self.message_user(request, f'{updated} refunds marked as processing.')
    process_refunds.short_description = "Process selected refunds"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(
            status='completed',
            processed_at=timezone.now()
        )
        self.message_user(request, f'{updated} refunds marked as completed.')
    mark_as_completed.short_description = "Mark selected refunds as completed"
    
    def mark_as_failed(self, request, queryset):
        updated = queryset.update(status='failed')
        self.message_user(request, f'{updated} refunds marked as failed.')
    mark_as_failed.short_description = "Mark selected refunds as failed"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('transaction', 'user')


@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'gateway_type', 'is_active', 'is_test_mode',
        'processing_fee_percentage', 'processing_fee_fixed', 'created_at'
    ]
    list_filter = [
        'gateway_type', 'is_active', 'is_test_mode', 'created_at'
    ]
    search_fields = [
        'name', 'description', 'api_url', 'webhook_url'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at'
    ]
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'gateway_type', 'is_active', 'is_test_mode')
        }),
        ('Configuration', {
            'fields': ('api_key', 'secret_key', 'webhook_secret'),
            'classes': ('collapse',)
        }),
        ('URLs', {
            'fields': ('api_url', 'webhook_url'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('supported_currencies', 'supported_payment_methods'),
            'classes': ('collapse',)
        }),
        ('Fees', {
            'fields': ('processing_fee_percentage', 'processing_fee_fixed'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('description', 'metadata'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_gateways', 'deactivate_gateways', 'enable_test_mode', 'disable_test_mode']
    
    def activate_gateways(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} payment gateways activated.')
    activate_gateways.short_description = "Activate selected gateways"
    
    def deactivate_gateways(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} payment gateways deactivated.')
    deactivate_gateways.short_description = "Deactivate selected gateways"
    
    def enable_test_mode(self, request, queryset):
        updated = queryset.update(is_test_mode=True)
        self.message_user(request, f'{updated} payment gateways enabled for test mode.')
    enable_test_mode.short_description = "Enable test mode for selected gateways"
    
    def disable_test_mode(self, request, queryset):
        updated = queryset.update(is_test_mode=False)
        self.message_user(request, f'{updated} payment gateways disabled for test mode.')
    disable_test_mode.short_description = "Disable test mode for selected gateways"


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'transaction', 'level', 'message', 'gateway', 'created_at'
    ]
    list_filter = [
        'level', 'gateway', 'created_at'
    ]
    search_fields = [
        'message', 'transaction__transaction_id', 'gateway__name'
    ]
    readonly_fields = [
        'id', 'created_at'
    ]
    list_select_related = ['transaction', 'gateway']
    list_per_page = 100
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'transaction', 'gateway', 'level')
        }),
        ('Log Details', {
            'fields': ('message', 'details')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['clear_old_logs']
    
    def clear_old_logs(self, request, queryset):
        from datetime import timedelta
        cutoff_date = timezone.now() - timedelta(days=30)
        deleted, _ = PaymentLog.objects.filter(created_at__lt=cutoff_date).delete()
        self.message_user(request, f'{deleted} old payment logs deleted.')
    clear_old_logs.short_description = "Clear logs older than 30 days"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('transaction', 'gateway')
