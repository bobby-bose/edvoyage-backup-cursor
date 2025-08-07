from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentMethodViewSet,
    PaymentTransactionViewSet,
    SubscriptionViewSet,
    InvoiceViewSet,
    RefundViewSet,
    PaymentGatewayViewSet,
    PaymentLogViewSet,
    PaymentStatsViewSet,
)

# Create the main router
router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet, basename='paymentmethod')
router.register(r'transactions', PaymentTransactionViewSet, basename='paymenttransaction')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'refunds', RefundViewSet, basename='refund')
router.register(r'gateways', PaymentGatewayViewSet, basename='paymentgateway')
router.register(r'logs', PaymentLogViewSet, basename='paymentlog')
router.register(r'stats', PaymentStatsViewSet, basename='paymentstats')

# URL patterns
urlpatterns = [
    # Main API endpoints
    path('api/payments/', include(router.urls)),
    
    # Payment method specific endpoints
    path('api/payments/payment-methods/<uuid:pk>/set-default/',
         PaymentMethodViewSet.as_view({'post': 'set_default'}),
         name='paymentmethod-set-default'),
    
    path('api/payments/payment-methods/<uuid:pk>/activate/',
         PaymentMethodViewSet.as_view({'post': 'activate'}),
         name='paymentmethod-activate'),
    
    path('api/payments/payment-methods/<uuid:pk>/deactivate/',
         PaymentMethodViewSet.as_view({'post': 'deactivate'}),
         name='paymentmethod-deactivate'),
    
    path('api/payments/payment-methods/defaults/',
         PaymentMethodViewSet.as_view({'get': 'defaults'}),
         name='paymentmethod-defaults'),
    
    path('api/payments/payment-methods/stats/',
         PaymentMethodViewSet.as_view({'get': 'stats'}),
         name='paymentmethod-stats'),
    
    # Transaction specific endpoints
    path('api/payments/transactions/<uuid:pk>/process/',
         PaymentTransactionViewSet.as_view({'post': 'process_payment'}),
         name='transaction-process'),
    
    path('api/payments/transactions/<uuid:pk>/cancel/',
         PaymentTransactionViewSet.as_view({'post': 'cancel_transaction'}),
         name='transaction-cancel'),
    
    path('api/payments/transactions/<uuid:pk>/request-refund/',
         PaymentTransactionViewSet.as_view({'post': 'request_refund'}),
         name='transaction-request-refund'),
    
    path('api/payments/transactions/stats/',
         PaymentTransactionViewSet.as_view({'get': 'stats'}),
         name='transaction-stats'),
    
    path('api/payments/transactions/recent/',
         PaymentTransactionViewSet.as_view({'get': 'recent'}),
         name='transaction-recent'),
    
    # Subscription specific endpoints
    path('api/payments/subscriptions/<uuid:pk>/cancel/',
         SubscriptionViewSet.as_view({'post': 'cancel_subscription'}),
         name='subscription-cancel'),
    
    path('api/payments/subscriptions/<uuid:pk>/renew/',
         SubscriptionViewSet.as_view({'post': 'renew_subscription'}),
         name='subscription-renew'),
    
    path('api/payments/subscriptions/<uuid:pk>/change-payment-method/',
         SubscriptionViewSet.as_view({'post': 'change_payment_method'}),
         name='subscription-change-payment-method'),
    
    path('api/payments/subscriptions/active/',
         SubscriptionViewSet.as_view({'get': 'active'}),
         name='subscription-active'),
    
    path('api/payments/subscriptions/expiring-soon/',
         SubscriptionViewSet.as_view({'get': 'expiring_soon'}),
         name='subscription-expiring-soon'),
    
    path('api/payments/subscriptions/stats/',
         SubscriptionViewSet.as_view({'get': 'stats'}),
         name='subscription-stats'),
    
    # Invoice specific endpoints
    path('api/payments/invoices/<uuid:pk>/mark-paid/',
         InvoiceViewSet.as_view({'post': 'mark_as_paid'}),
         name='invoice-mark-paid'),
    
    path('api/payments/invoices/<uuid:pk>/download-pdf/',
         InvoiceViewSet.as_view({'get': 'download_pdf'}),
         name='invoice-download-pdf'),
    
    path('api/payments/invoices/overdue/',
         InvoiceViewSet.as_view({'get': 'overdue'}),
         name='invoice-overdue'),
    
    path('api/payments/invoices/stats/',
         InvoiceViewSet.as_view({'get': 'stats'}),
         name='invoice-stats'),
    
    # Refund specific endpoints
    path('api/payments/refunds/<uuid:pk>/process/',
         RefundViewSet.as_view({'post': 'process_refund'}),
         name='refund-process'),
    
    path('api/payments/refunds/stats/',
         RefundViewSet.as_view({'get': 'stats'}),
         name='refund-stats'),
    
    # Gateway specific endpoints
    path('api/payments/gateways/supported-methods/',
         PaymentGatewayViewSet.as_view({'get': 'supported_methods'}),
         name='gateway-supported-methods'),
    
    # Log specific endpoints
    path('api/payments/logs/errors/',
         PaymentLogViewSet.as_view({'get': 'errors'}),
         name='paymentlog-errors'),
    
    # Stats specific endpoints
    path('api/payments/stats/overview/',
         PaymentStatsViewSet.as_view({'get': 'overview'}),
         name='paymentstats-overview'),
    
    path('api/payments/stats/trends/',
         PaymentStatsViewSet.as_view({'get': 'trends'}),
         name='paymentstats-trends'),
    
    # Additional payment processing endpoints
    path('api/payments/process/',
         PaymentTransactionViewSet.as_view({'post': 'create'}),
         name='payment-process'),
    
    path('api/payments/verify/',
         PaymentTransactionViewSet.as_view({'post': 'create'}),
         name='payment-verify'),
    
    path('api/payments/webhook/stripe/',
         PaymentTransactionViewSet.as_view({'post': 'create'}),
         name='webhook-stripe'),
    
    path('api/payments/webhook/paypal/',
         PaymentTransactionViewSet.as_view({'post': 'create'}),
         name='webhook-paypal'),
    
    path('api/payments/webhook/razorpay/',
         PaymentTransactionViewSet.as_view({'post': 'create'}),
         name='webhook-razorpay'),
    
    # Payment method management endpoints
    path('api/payments/payment-methods/add-card/',
         PaymentMethodViewSet.as_view({'post': 'create'}),
         name='paymentmethod-add-card'),
    
    path('api/payments/payment-methods/add-bank/',
         PaymentMethodViewSet.as_view({'post': 'create'}),
         name='paymentmethod-add-bank'),
    
    path('api/payments/payment-methods/add-wallet/',
         PaymentMethodViewSet.as_view({'post': 'create'}),
         name='paymentmethod-add-wallet'),
    
    # Subscription management endpoints
    path('api/payments/subscriptions/create/',
         SubscriptionViewSet.as_view({'post': 'create'}),
         name='subscription-create'),
    
    path('api/payments/subscriptions/upgrade/',
         SubscriptionViewSet.as_view({'post': 'create'}),
         name='subscription-upgrade'),
    
    path('api/payments/subscriptions/downgrade/',
         SubscriptionViewSet.as_view({'post': 'create'}),
         name='subscription-downgrade'),
    
    # Billing endpoints
    path('api/payments/billing/history/',
         PaymentTransactionViewSet.as_view({'get': 'list'}),
         name='billing-history'),
    
    path('api/payments/billing/upcoming/',
         InvoiceViewSet.as_view({'get': 'list'}),
         name='billing-upcoming'),
    
    path('api/payments/billing/summary/',
         PaymentStatsViewSet.as_view({'get': 'overview'}),
         name='billing-summary'),
    
    # Payment security endpoints
    path('api/payments/security/verify-payment-method/',
         PaymentMethodViewSet.as_view({'post': 'create'}),
         name='security-verify-payment-method'),
    
    path('api/payments/security/validate-transaction/',
         PaymentTransactionViewSet.as_view({'post': 'create'}),
         name='security-validate-transaction'),
    
    # Payment analytics endpoints
    path('api/payments/analytics/spending-patterns/',
         PaymentStatsViewSet.as_view({'get': 'overview'}),
         name='analytics-spending-patterns'),
    
    path('api/payments/analytics/payment-methods-usage/',
         PaymentStatsViewSet.as_view({'get': 'overview'}),
         name='analytics-payment-methods-usage'),
    
    path('api/payments/analytics/subscription-metrics/',
         PaymentStatsViewSet.as_view({'get': 'overview'}),
         name='analytics-subscription-metrics'),
    
    # Payment support endpoints
    path('api/payments/support/transaction-issues/',
         PaymentTransactionViewSet.as_view({'get': 'list'}),
         name='support-transaction-issues'),
    
    path('api/payments/support/refund-requests/',
         RefundViewSet.as_view({'get': 'list'}),
         name='support-refund-requests'),
    
    path('api/payments/support/payment-disputes/',
         PaymentTransactionViewSet.as_view({'get': 'list'}),
         name='support-payment-disputes'),
] 