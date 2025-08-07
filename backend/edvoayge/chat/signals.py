from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageStatus, Contact, ChatNotification


@receiver(post_save, sender=Message)
def create_message_notifications(sender, instance, created, **kwargs):
    """Create notifications when a new message is sent"""
    if created:
        # Get all participants in the room except the sender
        participants = instance.room.participants.filter(
            is_active=True
        ).exclude(user=instance.sender)
        
        # Create notifications for each participant
        for participant in participants:
            notification_type = 'message_reply' if instance.reply_to else 'new_message'
            ChatNotification.objects.create(
                user=participant.user,
                message=instance,
                type=notification_type
            )


@receiver(post_save, sender=MessageStatus)
def update_message_delivery_status(sender, instance, created, **kwargs):
    """Update message delivery status"""
    if created:
        # Update status to 'delivered' when message status is created
        if instance.status == 'sent':
            # In a real implementation, you might want to add logic here
            # to mark as 'delivered' after a certain time
            pass


@receiver(post_save, sender=Contact)
def create_contact_notification(sender, instance, created, **kwargs):
    """Create notification when someone adds a contact"""
    if created:
        # Create a notification for the contact being added
        ChatNotification.objects.create(
            user=instance.contact,
            message=None,
            type='contact_request'
        )


@receiver(post_delete, sender=Message)
def delete_message_notifications(sender, instance, **kwargs):
    """Delete notifications when a message is deleted"""
    # Delete all notifications related to this message
    ChatNotification.objects.filter(message=instance).delete()


@receiver(post_delete, sender=Contact)
def delete_contact_notifications(sender, instance, **kwargs):
    """Delete contact-related notifications when contact is removed"""
    # Delete contact request notifications
    ChatNotification.objects.filter(
        user=instance.contact,
        type='contact_request'
    ).delete()


# Additional signals for real-time features
@receiver(post_save, sender=Message)
def update_room_last_activity(sender, instance, created, **kwargs):
    """Update room's last activity timestamp"""
    if created:
        instance.room.updated_at = instance.created_at
        instance.room.save(update_fields=['updated_at'])


@receiver(post_save, sender=ChatNotification)
def mark_notification_as_unread(sender, instance, created, **kwargs):
    """Ensure new notifications are marked as unread"""
    if created:
        instance.is_read = False
        instance.save(update_fields=['is_read']) 