from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post, Comment, PostLike, CommentLike, PostShare, Notification, UserFollow


@receiver(post_save, sender=PostLike)
def create_post_like_notification(sender, instance, created, **kwargs):
    """Create notification when someone likes a post"""
    if created:
        # Don't notify if user likes their own post
        if instance.user != instance.post.author:
            Notification.objects.create(
                recipient=instance.post.author,
                sender=instance.user,
                notification_type='like',
                post=instance.post,
                message=f"{instance.user.username} liked your post"
            )


@receiver(post_save, sender=CommentLike)
def create_comment_like_notification(sender, instance, created, **kwargs):
    """Create notification when someone likes a comment"""
    if created:
        # Don't notify if user likes their own comment
        if instance.user != instance.comment.author:
            Notification.objects.create(
                recipient=instance.comment.author,
                sender=instance.user,
                notification_type='like',
                comment=instance.comment,
                message=f"{instance.user.username} liked your comment"
            )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Create notification when someone comments on a post"""
    if created:
        # Don't notify if user comments on their own post
        if instance.author != instance.post.author:
            Notification.objects.create(
                recipient=instance.post.author,
                sender=instance.author,
                notification_type='comment',
                post=instance.post,
                message=f"{instance.author.username} commented on your post"
            )


@receiver(post_save, sender=PostShare)
def create_share_notification(sender, instance, created, **kwargs):
    """Create notification when someone shares a post"""
    if created:
        # Don't notify if user shares their own post
        if instance.user != instance.post.author:
            Notification.objects.create(
                recipient=instance.post.author,
                sender=instance.user,
                notification_type='share',
                post=instance.post,
                message=f"{instance.user.username} shared your post"
            )


@receiver(post_save, sender=UserFollow)
def create_follow_notification(sender, instance, created, **kwargs):
    """Create notification when someone follows a user"""
    if created:
        Notification.objects.create(
            recipient=instance.following,
            sender=instance.follower,
            notification_type='follow',
            message=f"{instance.follower.username} started following you"
        )


@receiver(post_delete, sender=PostLike)
def delete_post_like_notification(sender, instance, **kwargs):
    """Delete notification when post like is removed"""
    Notification.objects.filter(
        recipient=instance.post.author,
        notification_type='like',
        post=instance.post
    ).delete()


@receiver(post_delete, sender=CommentLike)
def delete_comment_like_notification(sender, instance, **kwargs):
    """Delete notification when comment like is removed"""
    Notification.objects.filter(
        recipient=instance.comment.author,
        notification_type='like',
        comment=instance.comment
    ).delete()


@receiver(post_delete, sender=Comment)
def delete_comment_notification(sender, instance, **kwargs):
    """Delete notification when comment is deleted"""
    Notification.objects.filter(
        recipient=instance.post.author,
        notification_type='comment',
        post=instance.post
    ).delete()


@receiver(post_delete, sender=PostShare)
def delete_share_notification(sender, instance, **kwargs):
    """Delete notification when post share is deleted"""
    Notification.objects.filter(
        recipient=instance.post.author,
        notification_type='share',
        post=instance.post
    ).delete()


@receiver(post_delete, sender=UserFollow)
def delete_follow_notification(sender, instance, **kwargs):
    """Delete notification when follow is removed"""
    Notification.objects.filter(
        recipient=instance.following,
        notification_type='follow'
    ).delete() 