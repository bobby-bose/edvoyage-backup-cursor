from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    ChatUser, ChatRoom, ChatRoomParticipant, Message, 
    MessageStatus, Contact, ChatNotification
)
from .serializers import (
    ChatUserSerializer, ChatUserMinimalSerializer, ChatUserStatusSerializer,
    ChatRoomSerializer, ChatRoomCreateSerializer, ChatRoomParticipantSerializer,
    MessageSerializer, MessageCreateSerializer, MessageStatusSerializer,
    ContactSerializer, ContactCreateSerializer, ContactFavoriteSerializer,
    ContactBlockSerializer, ChatNotificationSerializer, ChatNotificationCreateSerializer,
    MessageReplySerializer, MessageSearchSerializer, UserSearchSerializer
)


class ChatUserViewSet(viewsets.ModelViewSet):
    """ViewSet for ChatUser management"""
    queryset = ChatUser.objects.all().order_by('-created_at')
    serializer_class = ChatUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role', 'institution', 'specialization', 'is_verified']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bio']

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        
        # Filter by role if provided
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role__icontains=role)
        
        # Filter by institution if provided
        institution = self.request.query_params.get('institution', None)
        if institution:
            queryset = queryset.filter(institution__icontains=institution)
        
        return queryset

    @action(detail=True, methods=['get', 'put', 'patch'])
    def status(self, request, pk=None):
        """Get or update user online status"""
        chat_user = self.get_object()
        
        if request.method == 'GET':
            serializer = ChatUserStatusSerializer(chat_user)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            serializer = ChatUserStatusSerializer(chat_user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search users with filters"""
        serializer = UserSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            query = serializer.validated_data.get('query', '')
            role = serializer.validated_data.get('role', '')
            institution = serializer.validated_data.get('institution', '')
            specialization = serializer.validated_data.get('specialization', '')
            is_verified = serializer.validated_data.get('is_verified', None)
            
            queryset = self.get_queryset()
            
            if query:
                queryset = queryset.filter(
                    Q(user__username__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(bio__icontains=query)
                )
            
            if role:
                queryset = queryset.filter(role__icontains=role)
            
            if institution:
                queryset = queryset.filter(institution__icontains=institution)
            
            if specialization:
                queryset = queryset.filter(specialization__icontains=specialization)
            
            if is_verified is not None:
                queryset = queryset.filter(is_verified=is_verified)
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = ChatUserMinimalSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = ChatUserMinimalSerializer(queryset, many=True)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatRoomViewSet(viewsets.ModelViewSet):
    """ViewSet for ChatRoom management"""
    queryset = ChatRoom.objects.all().order_by('-updated_at')
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'created_by']

    def get_queryset(self):
        """Filter rooms based on user participation"""
        user = self.request.user
        try:
            chat_user = ChatUser.objects.get(user=user)
            return ChatRoom.objects.filter(
                participants__user=chat_user,
                participants__is_active=True
            ).order_by('-updated_at')
        except ChatUser.DoesNotExist:
            return ChatRoom.objects.none()

    def perform_create(self, serializer):
        """Create room and add creator as participant"""
        room = serializer.save(created_by=self.request.user.chat_profile)
        ChatRoomParticipant.objects.create(
            room=room,
            user=self.request.user.chat_profile,
            role='admin'
        )

    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        """Get room participants"""
        room = self.get_object()
        participants = room.participants.filter(is_active=True)
        serializer = ChatRoomParticipantSerializer(participants, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add participant to room"""
        room = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            chat_user = ChatUser.objects.get(id=user_id)
            participant, created = ChatRoomParticipant.objects.get_or_create(
                room=room,
                user=chat_user,
                defaults={'role': 'member'}
            )
            
            if created:
                # Create notification for new participant
                ChatNotification.objects.create(
                    user=chat_user,
                    type='group_invite',
                    message=None
                )
            
            serializer = ChatRoomParticipantSerializer(participant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except ChatUser.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['delete'])
    def remove_participant(self, request, pk=None, user_id=None):
        """Remove participant from room"""
        room = self.get_object()
        
        try:
            participant = ChatRoomParticipant.objects.get(
                room=room,
                user_id=user_id
            )
            participant.is_active = False
            participant.left_at = timezone.now()
            participant.save()
            
            return Response({'message': 'Participant removed'}, status=status.HTTP_200_OK)
        
        except ChatRoomParticipant.DoesNotExist:
            return Response(
                {'error': 'Participant not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for Message management"""
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room', 'sender', 'message_type', 'is_edited']

    def get_queryset(self):
        """Filter messages based on user participation"""
        user = self.request.user
        try:
            chat_user = ChatUser.objects.get(user=user)
            return Message.objects.filter(
                room__participants__user=chat_user,
                room__participants__is_active=True
            ).order_by('-created_at')
        except ChatUser.DoesNotExist:
            return Message.objects.none()

    def perform_create(self, serializer):
        """Create message and set sender"""
        chat_user = ChatUser.objects.get(user=self.request.user)
        message = serializer.save(sender=chat_user)
        
        # Create message status for all room participants
        participants = message.room.participants.filter(is_active=True)
        for participant in participants:
            MessageStatus.objects.create(
                message=message,
                user=participant.user,
                status='sent'
            )
        
        # Create notifications for other participants
        for participant in participants:
            if participant.user != chat_user:
                ChatNotification.objects.create(
                    user=participant.user,
                    message=message,
                    type='new_message'
                )

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """Reply to a message"""
        original_message = self.get_object()
        chat_user = ChatUser.objects.get(user=request.user)
        
        serializer = MessageReplySerializer(data=request.data)
        if serializer.is_valid():
            reply_message = serializer.save(
                room=original_message.room,
                sender=chat_user,
                reply_to=original_message
            )
            
            # Create message status for all room participants
            participants = reply_message.room.participants.filter(is_active=True)
            for participant in participants:
                MessageStatus.objects.create(
                    message=reply_message,
                    user=participant.user,
                    status='sent'
                )
            
            # Create notifications for other participants
            for participant in participants:
                if participant.user != chat_user:
                    ChatNotification.objects.create(
                        user=participant.user,
                        message=reply_message,
                        type='message_reply'
                    )
            
            return Response(MessageSerializer(reply_message).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search messages"""
        serializer = MessageSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            query = serializer.validated_data.get('query', '')
            room_id = serializer.validated_data.get('room_id')
            message_type = serializer.validated_data.get('message_type')
            date_from = serializer.validated_data.get('date_from')
            date_to = serializer.validated_data.get('date_to')
            
            queryset = self.get_queryset()
            
            if query:
                queryset = queryset.filter(content__icontains=query)
            
            if room_id:
                queryset = queryset.filter(room_id=room_id)
            
            if message_type:
                queryset = queryset.filter(message_type=message_type)
            
            if date_from:
                queryset = queryset.filter(created_at__date__gte=date_from)
            
            if date_to:
                queryset = queryset.filter(created_at__date__lte=date_to)
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = MessageSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = MessageSerializer(queryset, many=True)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageStatusViewSet(viewsets.ModelViewSet):
    """ViewSet for MessageStatus management"""
    queryset = MessageStatus.objects.all()
    serializer_class = MessageStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark message as read"""
        message_status = self.get_object()
        message_status.status = 'read'
        message_status.save()
        
        return Response({'message': 'Message marked as read'}, status=status.HTTP_200_OK)


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet for Contact management"""
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter contacts for current user"""
        user = self.request.user
        try:
            chat_user = ChatUser.objects.get(user=user)
            return Contact.objects.filter(user=chat_user).order_by('-created_at')
        except ChatUser.DoesNotExist:
            return Contact.objects.none()

    def perform_create(self, serializer):
        """Create contact for current user"""
        chat_user = ChatUser.objects.get(user=self.request.user)
        serializer.save(user=chat_user)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """Toggle contact favorite status"""
        contact = self.get_object()
        contact.is_favorite = not contact.is_favorite
        contact.save()
        
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        """Toggle contact block status"""
        contact = self.get_object()
        contact.is_blocked = not contact.is_blocked
        contact.save()
        
        serializer = ContactSerializer(contact)
        return Response(serializer.data)


class ChatNotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for ChatNotification management"""
    queryset = ChatNotification.objects.all().order_by('-created_at')
    serializer_class = ChatNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter notifications for current user"""
        user = self.request.user
        try:
            chat_user = ChatUser.objects.get(user=user)
            return ChatNotification.objects.filter(user=chat_user).order_by('-created_at')
        except ChatUser.DoesNotExist:
            return ChatNotification.objects.none()

    @action(detail=True, methods=['put', 'patch'])
    def read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        
        serializer = ChatNotificationSerializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def read_all(self, request):
        """Mark all notifications as read"""
        user = self.request.user
        try:
            chat_user = ChatUser.objects.get(user=user)
            ChatNotification.objects.filter(user=chat_user).update(is_read=True)
            return Response({'message': 'All notifications marked as read'}, status=status.HTTP_200_OK)
        except ChatUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get unread notification count"""
        user = self.request.user
        try:
            chat_user = ChatUser.objects.get(user=user)
            count = ChatNotification.objects.filter(user=chat_user, is_read=False).count()
            return Response({'unread_count': count})
        except ChatUser.DoesNotExist:
            return Response({'unread_count': 0})


class SearchViewSet(viewsets.ViewSet):
    """ViewSet for search functionality"""
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def users(self, request):
        """Search users"""
        serializer = UserSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            query = serializer.validated_data.get('query', '')
            role = serializer.validated_data.get('role', '')
            institution = serializer.validated_data.get('institution', '')
            specialization = serializer.validated_data.get('specialization', '')
            is_verified = serializer.validated_data.get('is_verified', None)
            
            queryset = ChatUser.objects.all()
            
            if query:
                queryset = queryset.filter(
                    Q(user__username__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(bio__icontains=query)
                )
            
            if role:
                queryset = queryset.filter(role__icontains=role)
            
            if institution:
                queryset = queryset.filter(institution__icontains=institution)
            
            if specialization:
                queryset = queryset.filter(specialization__icontains=specialization)
            
            if is_verified is not None:
                queryset = queryset.filter(is_verified=is_verified)
            
            serializer = ChatUserMinimalSerializer(queryset, many=True)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def messages(self, request):
        """Search messages"""
        serializer = MessageSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            query = serializer.validated_data.get('query', '')
            room_id = serializer.validated_data.get('room_id')
            message_type = serializer.validated_data.get('message_type')
            date_from = serializer.validated_data.get('date_from')
            date_to = serializer.validated_data.get('date_to')
            
            # Get user's accessible rooms
            user = self.request.user
            try:
                chat_user = ChatUser.objects.get(user=user)
                accessible_rooms = ChatRoom.objects.filter(
                    participants__user=chat_user,
                    participants__is_active=True
                )
                
                queryset = Message.objects.filter(room__in=accessible_rooms)
                
                if query:
                    queryset = queryset.filter(content__icontains=query)
                
                if room_id:
                    queryset = queryset.filter(room_id=room_id)
                
                if message_type:
                    queryset = queryset.filter(message_type=message_type)
                
                if date_from:
                    queryset = queryset.filter(created_at__date__gte=date_from)
                
                if date_to:
                    queryset = queryset.filter(created_at__date__lte=date_to)
                
                serializer = MessageSerializer(queryset, many=True)
                return Response(serializer.data)
            
            except ChatUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
