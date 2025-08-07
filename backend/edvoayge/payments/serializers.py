from rest_framework import serializers
from django.contrib.auth import get_user_model
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

User = get_user_model()


class PaymentMethodSerializer(serializers.ModelSerializer):
    """Serializer for payment methods"""
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    masked_card_number = serializers.SerializerMethodField()
    masked_account_number = serializers.SerializerMethodField()
    
    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'user', 'payment_type', 'payment_type_display', 'name',
            'is_default', 'is_active', 'card_last4', 'card_brand',
            'card_exp_month', 'card_exp_year', 'bank_name', 'account_last4',
            'account_type', 'wallet_type', 'masked_card_number',
            'masked_account_number', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_masked_card_number(self, obj):
        """Return masked card number for display"""
        if obj.card_last4:
            return f"**** **** **** {obj.card_last4}"
        return None
    
    def get_masked_account_number(self, obj):
        """Return masked account number for display"""
        if obj.account_last4:
            return f"**** {obj.account_last4}"
        return None
    
    def validate(self, data):
        """Validate payment method data"""
        payment_type = data.get('payment_type')
        
        # Validate card-specific fields
        if payment_type in ['credit_card', 'debit_card']:
            if not data.get('card_last4'):
                raise serializers.ValidationError("Card last 4 digits are required for card payments")
            if not data.get('card_brand'):
                raise serializers.ValidationError("Card brand is required for card payments")
        
        # Validate bank account fields
        elif payment_type == 'bank_transfer':
            if not data.get('bank_name'):
                raise serializers.ValidationError("Bank name is required for bank transfers")
            if not data.get('account_last4'):
                raise serializers.ValidationError("Account last 4 digits are required for bank transfers")
        
        # Validate digital wallet fields
        elif payment_type in ['paypal', 'stripe', 'razorpay', 'paytm']:
            if not data.get('wallet_type'):
                raise serializers.ValidationError("Wallet type is required for digital wallet payments")
        
        return data
    
    def create(self, validated_data):
        """Create payment method with user"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """Serializer for payment transactions"""
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    payment_method_details = PaymentMethodSerializer(source='payment_method', read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_successful = serializers.BooleanField(read_only=True)
    is_refundable = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'transaction_id', 'user', 'payment_method', 'payment_method_details',
            'transaction_type', 'transaction_type_display', 'amount', 'currency',
            'currency_display', 'status', 'status_display', 'related_object_type',
            'related_object_id', 'gateway', 'gateway_transaction_id', 'processing_fee',
            'tax_amount', 'discount_amount', 'total_amount', 'description',
            'is_successful', 'is_refundable', 'created_at', 'updated_at',
            'processed_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'transaction_id', 'user', 'gateway_transaction_id',
            'is_successful', 'is_refundable', 'created_at', 'updated_at',
            'processed_at', 'completed_at'
        ]
    
    def validate_amount(self, value):
        """Validate transaction amount"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value
    
    def validate(self, data):
        """Validate transaction data"""
        transaction_type = data.get('transaction_type')
        amount = data.get('amount')
        
        # Validate minimum amounts for different transaction types
        if transaction_type == 'subscription' and amount < 1.00:
            raise serializers.ValidationError("Subscription amount must be at least $1.00")
        
        if transaction_type == 'course_purchase' and amount < 5.00:
            raise serializers.ValidationError("Course purchase amount must be at least $5.00")
        
        return data
    
    def create(self, validated_data):
        """Create transaction with user and generate transaction ID"""
        user = self.context['request'].user
        validated_data['user'] = user
        
        # Generate unique transaction ID
        import uuid
        validated_data['transaction_id'] = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        
        return super().create(validated_data)


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for subscriptions"""
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    payment_method_details = PaymentMethodSerializer(source='payment_method', read_only=True)
    subscription_type_display = serializers.CharField(source='get_subscription_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    billing_cycle_display = serializers.CharField(source='get_billing_cycle_display', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_trial = serializers.BooleanField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'user', 'plan_name', 'subscription_type', 'subscription_type_display',
            'status', 'status_display', 'amount', 'currency', 'billing_cycle',
            'billing_cycle_display', 'start_date', 'end_date', 'trial_end_date',
            'cancelled_at', 'auto_renew', 'next_billing_date', 'payment_method',
            'payment_method_details', 'features', 'limits', 'description',
            'is_active', 'is_trial', 'days_remaining', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'is_active', 'is_trial', 'days_remaining',
            'created_at', 'updated_at'
        ]
    
    def validate(self, data):
        """Validate subscription data"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        trial_end_date = data.get('trial_end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date")
        
        if trial_end_date and start_date and trial_end_date <= start_date:
            raise serializers.ValidationError("Trial end date must be after start date")
        
        if trial_end_date and end_date and trial_end_date >= end_date:
            raise serializers.ValidationError("Trial end date must be before end date")
        
        return data
    
    def create(self, validated_data):
        """Create subscription with user"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for invoices"""
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    transaction_details = PaymentTransactionSerializer(source='transaction', read_only=True)
    subscription_details = SubscriptionSerializer(source='subscription', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'user', 'transaction', 'transaction_details',
            'subscription', 'subscription_details', 'status', 'status_display',
            'amount', 'currency', 'currency_display', 'billing_address',
            'shipping_address', 'issue_date', 'due_date', 'paid_date', 'items',
            'subtotal', 'tax_amount', 'discount_amount', 'total_amount', 'notes',
            'terms_conditions', 'is_overdue', 'days_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'invoice_number', 'user', 'transaction_details',
            'subscription_details', 'is_overdue', 'days_overdue',
            'created_at', 'updated_at'
        ]
    
    def validate(self, data):
        """Validate invoice data"""
        due_date = data.get('due_date')
        
        if due_date and due_date <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future")
        
        return data


class RefundSerializer(serializers.ModelSerializer):
    """Serializer for refunds"""
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    transaction_details = PaymentTransactionSerializer(source='transaction', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reason_display = serializers.CharField(source='get_reason_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    is_successful = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Refund
        fields = [
            'id', 'refund_id', 'transaction', 'transaction_details', 'user',
            'amount', 'currency', 'currency_display', 'status', 'status_display',
            'reason', 'reason_display', 'gateway_refund_id', 'notes',
            'is_successful', 'created_at', 'updated_at', 'processed_at'
        ]
        read_only_fields = [
            'id', 'refund_id', 'user', 'transaction_details', 'is_successful',
            'created_at', 'updated_at', 'processed_at'
        ]
    
    def validate_amount(self, value):
        """Validate refund amount"""
        if value <= 0:
            raise serializers.ValidationError("Refund amount must be greater than zero")
        return value
    
    def validate(self, data):
        """Validate refund data"""
        transaction = data.get('transaction')
        amount = data.get('amount')
        
        if transaction and amount:
            if amount > transaction.amount:
                raise serializers.ValidationError("Refund amount cannot exceed transaction amount")
            
            if not transaction.is_refundable:
                raise serializers.ValidationError("Transaction is not refundable")
        
        return data
    
    def create(self, validated_data):
        """Create refund with user and generate refund ID"""
        user = self.context['request'].user
        validated_data['user'] = user
        
        # Generate unique refund ID
        import uuid
        validated_data['refund_id'] = f"REF-{uuid.uuid4().hex[:8].upper()}"
        
        return super().create(validated_data)


class PaymentGatewaySerializer(serializers.ModelSerializer):
    """Serializer for payment gateways"""
    
    gateway_type_display = serializers.CharField(source='get_gateway_type_display', read_only=True)
    
    class Meta:
        model = PaymentGateway
        fields = [
            'id', 'name', 'gateway_type', 'gateway_type_display', 'is_active',
            'is_test_mode', 'api_url', 'webhook_url', 'supported_currencies',
            'supported_payment_methods', 'processing_fee_percentage',
            'processing_fee_fixed', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate gateway configuration"""
        gateway_type = data.get('gateway_type')
        
        # Validate required fields based on gateway type
        if gateway_type == 'stripe':
            if not data.get('api_key'):
                raise serializers.ValidationError("API key is required for Stripe")
        
        elif gateway_type == 'paypal':
            if not data.get('api_key'):
                raise serializers.ValidationError("Client ID is required for PayPal")
        
        return data


class PaymentLogSerializer(serializers.ModelSerializer):
    """Serializer for payment logs"""
    
    transaction_details = PaymentTransactionSerializer(source='transaction', read_only=True)
    gateway_details = PaymentGatewaySerializer(source='gateway', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    
    class Meta:
        model = PaymentLog
        fields = [
            'id', 'transaction', 'transaction_details', 'gateway', 'gateway_details',
            'level', 'level_display', 'message', 'details', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PaymentMethodCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating payment methods with encrypted data"""
    
    class Meta:
        model = PaymentMethod
        fields = [
            'payment_type', 'name', 'is_default', 'card_last4', 'card_brand',
            'card_exp_month', 'card_exp_year', 'bank_name', 'account_last4',
            'account_type', 'wallet_type', 'wallet_id', 'encrypted_data'
        ]
    
    def validate(self, data):
        """Validate payment method creation data"""
        payment_type = data.get('payment_type')
        
        # Validate required fields based on payment type
        if payment_type in ['credit_card', 'debit_card']:
            required_fields = ['card_last4', 'card_brand', 'card_exp_month', 'card_exp_year']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f"{field.replace('_', ' ').title()} is required for card payments")
        
        elif payment_type == 'bank_transfer':
            required_fields = ['bank_name', 'account_last4', 'account_type']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f"{field.replace('_', ' ').title()} is required for bank transfers")
        
        return data


class PaymentTransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating payment transactions"""
    
    class Meta:
        model = PaymentTransaction
        fields = [
            'payment_method', 'transaction_type', 'amount', 'currency',
            'related_object_type', 'related_object_id', 'description'
        ]
    
    def validate(self, data):
        """Validate transaction creation data"""
        transaction_type = data.get('transaction_type')
        amount = data.get('amount')
        
        # Validate minimum amounts
        min_amounts = {
            'subscription': 1.00,
            'course_purchase': 5.00,
            'consultation': 10.00,
            'application_fee': 25.00,
            'university_fee': 50.00,
        }
        
        if transaction_type in min_amounts and amount < min_amounts[transaction_type]:
            raise serializers.ValidationError(
                f"Minimum amount for {transaction_type} is ${min_amounts[transaction_type]:.2f}"
            )
        
        return data


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating subscriptions"""
    
    class Meta:
        model = Subscription
        fields = [
            'plan_name', 'subscription_type', 'amount', 'currency',
            'billing_cycle', 'start_date', 'end_date', 'trial_end_date',
            'auto_renew', 'payment_method', 'features', 'limits', 'description'
        ]
    
    def validate(self, data):
        """Validate subscription creation data"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date")
        
        return data


class PaymentStatsSerializer(serializers.Serializer):
    """Serializer for payment statistics"""
    
    total_transactions = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    successful_transactions = serializers.IntegerField()
    failed_transactions = serializers.IntegerField()
    pending_transactions = serializers.IntegerField()
    refunded_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    processing_fees = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    period = serializers.CharField()
    date_range = serializers.ListField(child=serializers.CharField())


class PaymentMethodStatsSerializer(serializers.Serializer):
    """Serializer for payment method statistics"""
    
    payment_type = serializers.CharField()
    count = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    success_rate = serializers.FloatField()
    average_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class SubscriptionStatsSerializer(serializers.Serializer):
    """Serializer for subscription statistics"""
    
    active_subscriptions = serializers.IntegerField()
    cancelled_subscriptions = serializers.IntegerField()
    trial_subscriptions = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_subscription_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    churn_rate = serializers.FloatField()
    renewal_rate = serializers.FloatField() 