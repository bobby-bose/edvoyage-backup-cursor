import uuid
import logging
from datetime import timedelta
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    PaymentMethod,
    PaymentTransaction,
    Subscription,
    Invoice,
    Refund,
    PaymentGateway,
    PaymentLog,
)
from .serializers import (
    PaymentMethodSerializer,
    PaymentTransactionSerializer,
    SubscriptionSerializer,
    InvoiceSerializer,
    RefundSerializer,
    PaymentGatewaySerializer,
    PaymentLogSerializer,
    PaymentMethodCreateSerializer,
    PaymentTransactionCreateSerializer,
    SubscriptionCreateSerializer,
    PaymentStatsSerializer,
    PaymentMethodStatsSerializer,
    SubscriptionStatsSerializer,
)

logger = logging.getLogger(__name__)


class PaymentMethodViewSet(viewsets.ModelViewSet):
    """ViewSet for payment methods"""
    
    serializer_class = PaymentMethodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_type', 'is_default', 'is_active']
    search_fields = ['name', 'card_brand', 'bank_name']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-is_default', '-created_at']
    
    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentMethodCreateSerializer
        return PaymentMethodSerializer
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Set payment method as default"""
        payment_method = self.get_object()
        
        # Remove default from other payment methods
        PaymentMethod.objects.filter(
            user=request.user, is_default=True
        ).exclude(id=payment_method.id).update(is_default=False)
        
        payment_method.is_default = True
        payment_method.save()
        
        serializer = self.get_serializer(payment_method)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate payment method"""
        payment_method = self.get_object()
        payment_method.is_active = False
        payment_method.save()
        
        serializer = self.get_serializer(payment_method)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate payment method"""
        payment_method = self.get_object()
        payment_method.is_active = True
        payment_method.save()
        
        serializer = self.get_serializer(payment_method)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def defaults(self, request):
        """Get default payment methods by type"""
        default_methods = PaymentMethod.objects.filter(
            user=request.user, is_default=True, is_active=True
        )
        serializer = self.get_serializer(default_methods, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get payment method statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total_methods': queryset.count(),
            'active_methods': queryset.filter(is_active=True).count(),
            'default_methods': queryset.filter(is_default=True).count(),
            'by_type': queryset.values('payment_type').annotate(
                count=Count('id')
            )
        }
        
        return Response(stats)


class PaymentTransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for payment transactions"""
    
    serializer_class = PaymentTransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'status', 'currency', 'gateway']
    search_fields = ['transaction_id', 'description', 'gateway_transaction_id']
    ordering_fields = ['created_at', 'amount', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentTransactionCreateSerializer
        return PaymentTransactionSerializer
    
    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        """Process payment transaction"""
        transaction = self.get_object()
        
        if transaction.status != 'pending':
            return Response(
                {'error': 'Transaction is not in pending status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Simulate payment processing
        try:
            transaction.status = 'processing'
            transaction.save()
            
            # Log the processing attempt
            PaymentLog.objects.create(
                transaction=transaction,
                level='info',
                message='Payment processing started',
                details={'user_id': request.user.id}
            )
            
            # Simulate successful payment
            transaction.status = 'completed'
            transaction.processed_at = timezone.now()
            transaction.completed_at = timezone.now()
            transaction.save()
            
            PaymentLog.objects.create(
                transaction=transaction,
                level='info',
                message='Payment completed successfully',
                details={'user_id': request.user.id}
            )
            
            serializer = self.get_serializer(transaction)
            return Response(serializer.data)
            
        except Exception as e:
            transaction.status = 'failed'
            transaction.save()
            
            PaymentLog.objects.create(
                transaction=transaction,
                level='error',
                message=f'Payment processing failed: {str(e)}',
                details={'user_id': request.user.id, 'error': str(e)}
            )
            
            return Response(
                {'error': 'Payment processing failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def cancel_transaction(self, request, pk=None):
        """Cancel pending transaction"""
        transaction = self.get_object()
        
        if transaction.status not in ['pending', 'processing']:
            return Response(
                {'error': 'Transaction cannot be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.status = 'cancelled'
        transaction.save()
        
        PaymentLog.objects.create(
            transaction=transaction,
            level='info',
            message='Transaction cancelled by user',
            details={'user_id': request.user.id}
        )
        
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def request_refund(self, request, pk=None):
        """Request refund for transaction"""
        transaction = self.get_object()
        
        if not transaction.is_refundable:
            return Response(
                {'error': 'Transaction is not refundable'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        amount = request.data.get('amount', transaction.amount)
        reason = request.data.get('reason', 'requested_by_customer')
        notes = request.data.get('notes', '')
        
        if amount > transaction.amount:
            return Response(
                {'error': 'Refund amount cannot exceed transaction amount'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refund = Refund.objects.create(
            transaction=transaction,
            user=request.user,
            amount=amount,
            currency=transaction.currency,
            reason=reason,
            notes=notes
        )
        
        serializer = RefundSerializer(refund)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get transaction statistics"""
        queryset = self.get_queryset()
        
        # Date range filter
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        queryset = queryset.filter(created_at__gte=start_date)
        
        stats = {
            'total_transactions': queryset.count(),
            'total_amount': queryset.aggregate(total=Sum('amount'))['total'] or 0,
            'successful_transactions': queryset.filter(status='completed').count(),
            'failed_transactions': queryset.filter(status='failed').count(),
            'pending_transactions': queryset.filter(status='pending').count(),
            'by_status': queryset.values('status').annotate(
                count=Count('id'),
                total_amount=Sum('amount')
            ),
            'by_type': queryset.values('transaction_type').annotate(
                count=Count('id'),
                total_amount=Sum('amount')
            ),
            'by_currency': queryset.values('currency').annotate(
                count=Count('id'),
                total_amount=Sum('amount')
            )
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent transactions"""
        limit = int(request.query_params.get('limit', 10))
        queryset = self.get_queryset().order_by('-created_at')[:limit]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet for subscriptions"""
    
    serializer_class = SubscriptionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subscription_type', 'status', 'currency', 'auto_renew']
    search_fields = ['plan_name', 'description']
    ordering_fields = ['created_at', 'amount', 'status', 'end_date']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SubscriptionCreateSerializer
        return SubscriptionSerializer
    
    @action(detail=True, methods=['post'])
    def cancel_subscription(self, request, pk=None):
        """Cancel subscription"""
        subscription = self.get_object()
        
        if subscription.status not in ['active', 'trial']:
            return Response(
                {'error': 'Subscription cannot be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscription.status = 'cancelled'
        subscription.cancelled_at = timezone.now()
        subscription.auto_renew = False
        subscription.save()
        
        serializer = self.get_serializer(subscription)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def renew_subscription(self, request, pk=None):
        """Renew subscription"""
        subscription = self.get_object()
        
        if subscription.status != 'cancelled':
            return Response(
                {'error': 'Subscription is not cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscription.status = 'active'
        subscription.cancelled_at = None
        subscription.auto_renew = True
        subscription.save()
        
        serializer = self.get_serializer(subscription)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def change_payment_method(self, request, pk=None):
        """Change subscription payment method"""
        subscription = self.get_object()
        payment_method_id = request.data.get('payment_method_id')
        
        if not payment_method_id:
            return Response(
                {'error': 'Payment method ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            payment_method = PaymentMethod.objects.get(
                id=payment_method_id, user=request.user
            )
            subscription.payment_method = payment_method
            subscription.save()
            
            serializer = self.get_serializer(subscription)
            return Response(serializer.data)
            
        except PaymentMethod.DoesNotExist:
            return Response(
                {'error': 'Payment method not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active subscriptions"""
        queryset = self.get_queryset().filter(status='active')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get subscriptions expiring soon"""
        days = int(request.query_params.get('days', 7))
        end_date = timezone.now() + timedelta(days=days)
        
        queryset = self.get_queryset().filter(
            status='active',
            end_date__lte=end_date
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get subscription statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total_subscriptions': queryset.count(),
            'active_subscriptions': queryset.filter(status='active').count(),
            'trial_subscriptions': queryset.filter(status='trial').count(),
            'cancelled_subscriptions': queryset.filter(status='cancelled').count(),
            'total_revenue': queryset.filter(status='active').aggregate(
                total=Sum('amount')
            )['total'] or 0,
            'average_subscription_value': queryset.filter(status='active').aggregate(
                avg=Avg('amount')
            )['avg'] or 0,
            'by_type': queryset.values('subscription_type').annotate(
                count=Count('id'),
                total_amount=Sum('amount')
            ),
            'by_status': queryset.values('status').annotate(
                count=Count('id'),
                total_amount=Sum('amount')
            )
        }
        
        return Response(stats)


class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for invoices"""
    
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'currency']
    search_fields = ['invoice_number', 'notes']
    ordering_fields = ['created_at', 'due_date', 'amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """Mark invoice as paid"""
        invoice = self.get_object()
        
        if invoice.status == 'paid':
            return Response(
                {'error': 'Invoice is already paid'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        invoice.status = 'paid'
        invoice.paid_date = timezone.now()
        invoice.save()
        
        serializer = self.get_serializer(invoice)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Download invoice as PDF"""
        invoice = self.get_object()
        
        # This would generate and return a PDF file
        # For now, return a placeholder response
        return Response({
            'message': 'PDF download functionality would be implemented here',
            'invoice_number': invoice.invoice_number
        })
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue invoices"""
        queryset = self.get_queryset().filter(
            status__in=['sent', 'draft'],
            due_date__lt=timezone.now()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get invoice statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total_invoices': queryset.count(),
            'paid_invoices': queryset.filter(status='paid').count(),
            'overdue_invoices': queryset.filter(
                status__in=['sent', 'draft'],
                due_date__lt=timezone.now()
            ).count(),
            'total_amount': queryset.aggregate(total=Sum('total_amount'))['total'] or 0,
            'paid_amount': queryset.filter(status='paid').aggregate(
                total=Sum('total_amount')
            )['total'] or 0,
            'overdue_amount': queryset.filter(
                status__in=['sent', 'draft'],
                due_date__lt=timezone.now()
            ).aggregate(total=Sum('total_amount'))['total'] or 0,
            'by_status': queryset.values('status').annotate(
                count=Count('id'),
                total_amount=Sum('total_amount')
            )
        }
        
        return Response(stats)


class RefundViewSet(viewsets.ModelViewSet):
    """ViewSet for refunds"""
    
    serializer_class = RefundSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'reason', 'currency']
    search_fields = ['refund_id', 'notes']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Refund.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def process_refund(self, request, pk=None):
        """Process refund"""
        refund = self.get_object()
        
        if refund.status != 'pending':
            return Response(
                {'error': 'Refund is not in pending status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refund.status = 'processing'
            refund.save()
            
            # Simulate refund processing
            refund.status = 'completed'
            refund.processed_at = timezone.now()
            refund.save()
            
            # Update transaction status
            transaction = refund.transaction
            if refund.amount == transaction.amount:
                transaction.status = 'refunded'
            else:
                transaction.status = 'partially_refunded'
            transaction.save()
            
            serializer = self.get_serializer(refund)
            return Response(serializer.data)
            
        except Exception as e:
            refund.status = 'failed'
            refund.save()
            
            return Response(
                {'error': 'Refund processing failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get refund statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total_refunds': queryset.count(),
            'completed_refunds': queryset.filter(status='completed').count(),
            'pending_refunds': queryset.filter(status='pending').count(),
            'failed_refunds': queryset.filter(status='failed').count(),
            'total_amount': queryset.aggregate(total=Sum('amount'))['total'] or 0,
            'by_status': queryset.values('status').annotate(
                count=Count('id'),
                total_amount=Sum('amount')
            ),
            'by_reason': queryset.values('reason').annotate(
                count=Count('id'),
                total_amount=Sum('amount')
            )
        }
        
        return Response(stats)


class PaymentGatewayViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for payment gateways (read-only for users)"""
    
    serializer_class = PaymentGatewaySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gateway_type', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def get_queryset(self):
        return PaymentGateway.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'])
    def supported_methods(self, request):
        """Get supported payment methods by gateway"""
        gateways = self.get_queryset()
        
        methods = {}
        for gateway in gateways:
            methods[gateway.gateway_type] = {
                'name': gateway.name,
                'supported_currencies': gateway.supported_currencies,
                'supported_payment_methods': gateway.supported_payment_methods,
                'processing_fee_percentage': gateway.processing_fee_percentage,
                'processing_fee_fixed': gateway.processing_fee_fixed
            }
        
        return Response(methods)


class PaymentLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for payment logs (read-only)"""
    
    serializer_class = PaymentLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'gateway']
    search_fields = ['message']
    ordering_fields = ['created_at', 'level']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return PaymentLog.objects.filter(transaction__user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def errors(self, request):
        """Get error logs"""
        queryset = self.get_queryset().filter(level__in=['error', 'critical'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PaymentStatsViewSet(viewsets.ViewSet):
    """ViewSet for payment statistics"""
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get payment overview statistics"""
        user = request.user
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        transactions = PaymentTransaction.objects.filter(
            user=user, created_at__gte=start_date
        )
        
        subscriptions = Subscription.objects.filter(
            user=user, created_at__gte=start_date
        )
        
        stats = {
            'period': f'Last {days} days',
            'transactions': {
                'total': transactions.count(),
                'successful': transactions.filter(status='completed').count(),
                'failed': transactions.filter(status='failed').count(),
                'pending': transactions.filter(status='pending').count(),
                'total_amount': transactions.aggregate(total=Sum('amount'))['total'] or 0,
                'successful_amount': transactions.filter(status='completed').aggregate(
                    total=Sum('amount')
                )['total'] or 0
            },
            'subscriptions': {
                'active': subscriptions.filter(status='active').count(),
                'trial': subscriptions.filter(status='trial').count(),
                'cancelled': subscriptions.filter(status='cancelled').count(),
                'total_revenue': subscriptions.filter(status='active').aggregate(
                    total=Sum('amount')
                )['total'] or 0
            },
            'payment_methods': {
                'total': PaymentMethod.objects.filter(user=user, is_active=True).count(),
                'default': PaymentMethod.objects.filter(user=user, is_default=True).count()
            }
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Get payment trends over time"""
        user = request.user
        days = int(request.query_params.get('days', 30))
        
        # Get daily transaction amounts
        daily_transactions = PaymentTransaction.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timedelta(days=days)
        ).extra(
            select={'date': 'DATE(created_at)'}
        ).values('date').annotate(
            count=Count('id'),
            total_amount=Sum('amount')
        ).order_by('date')
        
        # Get daily subscription counts
        daily_subscriptions = Subscription.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timedelta(days=days)
        ).extra(
            select={'date': 'DATE(created_at)'}
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        trends = {
            'transactions': list(daily_transactions),
            'subscriptions': list(daily_subscriptions)
        }
        
        return Response(trends)
