# 💬 Chat - REST API Documentation

A comprehensive REST API for the Chat system, designed for medical students and professionals to communicate, share experiences, and connect with peers in real-time.

## 📋 **Features**

- ✅ **User Management** - Medical professional profiles with specializations
- ✅ **Real-time Messaging** - Direct and group chat functionality
- ✅ **Contact Management** - Add, favorite, and block contacts
- ✅ **Message Status Tracking** - Sent, delivered, read status
- ✅ **Notifications** - Real-time notifications for new messages
- ✅ **Search & Filtering** - Search users and messages
- ✅ **File Sharing** - Support for images, files, audio, video
- ✅ **Admin Interface** - Comprehensive Django admin for moderation

## 🗄️ **Database Models**

### **Core Models:**
- **ChatUser** - Extended user model with medical-specific fields
- **ChatRoom** - Direct and group chat rooms
- **ChatRoomParticipant** - Room membership management
- **Message** - Text, media, and file messages with replies
- **MessageStatus** - Message delivery status tracking
- **Contact** - Contact management with favorites/blocking
- **ChatNotification** - Real-time notifications

## 🌐 **API Endpoints**

### **🔐 Authentication & User Management**
```
GET    /api/v1/chat/api/users/                 # List chat users
GET    /api/v1/chat/api/users/{id}/            # Get user details
PUT    /api/v1/chat/api/users/{id}/            # Update user profile
GET    /api/v1/chat/api/users/{id}/status/     # Get user status
PUT    /api/v1/chat/api/users/{id}/status/     # Update user status
GET    /api/v1/chat/api/users/search/          # Search users
```

### **💬 Chat Rooms**
```
GET    /api/v1/chat/api/rooms/                 # List user's rooms
POST   /api/v1/chat/api/rooms/                 # Create new room
GET    /api/v1/chat/api/rooms/{id}/            # Get room details
PUT    /api/v1/chat/api/rooms/{id}/            # Update room
DELETE /api/v1/chat/api/rooms/{id}/            # Delete room
GET    /api/v1/chat/api/rooms/{id}/participants/ # Get room participants
POST   /api/v1/chat/api/rooms/{id}/add-participant/ # Add participant
DELETE /api/v1/chat/api/rooms/{id}/remove-participant/{user_id}/ # Remove participant
```

### **💭 Messages**
```
GET    /api/v1/chat/api/rooms/{room_id}/messages/ # Get room messages
POST   /api/v1/chat/api/rooms/{room_id}/messages/ # Send message
GET    /api/v1/chat/api/rooms/{room_id}/messages/{id}/ # Get message
PUT    /api/v1/chat/api/rooms/{room_id}/messages/{id}/ # Edit message
DELETE /api/v1/chat/api/rooms/{room_id}/messages/{id}/ # Delete message
POST   /api/v1/chat/api/messages/{id}/reply/   # Reply to message
GET    /api/v1/chat/api/messages/search/       # Search messages
```

### **📞 Contact Management**
```
GET    /api/v1/chat/api/contacts/              # List user's contacts
POST   /api/v1/chat/api/contacts/              # Add contact
GET    /api/v1/chat/api/contacts/{id}/         # Get contact details
PUT    /api/v1/chat/api/contacts/{id}/         # Update contact
DELETE /api/v1/chat/api/contacts/{id}/         # Remove contact
POST   /api/v1/chat/api/contacts/{id}/favorite/ # Toggle favorite
POST   /api/v1/chat/api/contacts/{id}/block/   # Toggle block
```

### **🔔 Notifications**
```
GET    /api/v1/chat/api/notifications/         # List notifications
PUT    /api/v1/chat/api/notifications/{id}/read/ # Mark as read
PUT    /api/v1/chat/api/notifications/read-all/ # Mark all as read
GET    /api/v1/chat/api/notifications/unread-count/ # Get unread count
```

### **🔍 Search**
```
GET    /api/v1/chat/api/search/users/?q={query} # Search users
GET    /api/v1/chat/api/search/messages/?q={query} # Search messages
```

## 📊 **API Response Examples**

### **ChatUser Response**
```json
{
  "id": "uuid",
  "user": {
    "id": "uuid",
    "username": "dr_aisha",
    "email": "aisha@example.com",
    "full_name": "Dr. Aisha Rehman"
  },
  "is_online": true,
  "last_seen": "2024-01-15T10:30:00Z",
  "profile_image": "https://example.com/image.jpg",
  "bio": "Medical student passionate about cardiology",
  "specialization": "Cardiology",
  "institution": "Amrita Institute of Medical Sciences",
  "role": "MBBS Student",
  "is_verified": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### **ChatRoom Response**
```json
{
  "id": "uuid",
  "name": "Direct Chat",
  "type": "direct",
  "created_by": {
    "id": "uuid",
    "user": {
      "id": "uuid",
      "username": "dr_aisha",
      "full_name": "Dr. Aisha Rehman"
    },
    "profile_image": "https://example.com/image.jpg",
    "specialization": "Cardiology",
    "institution": "Amrita Institute of Medical Sciences",
    "role": "MBBS Student",
    "is_online": true,
    "last_seen": "2024-01-15T10:30:00Z"
  },
  "participants": [
    {
      "id": "uuid",
      "user": {
        "id": "uuid",
        "username": "dr_aisha",
        "full_name": "Dr. Aisha Rehman",
        "profile_image": "https://example.com/image.jpg"
      },
      "role": "admin",
      "joined_at": "2024-01-15T10:30:00Z",
      "left_at": null,
      "is_active": true
    }
  ],
  "last_message": {
    "id": "uuid",
    "content": "Hello! How are you?",
    "sender": "uuid",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "unread_count": 3,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### **Message Response**
```json
{
  "id": "uuid",
  "room": "uuid",
  "sender": {
    "id": "uuid",
    "user": {
      "id": "uuid",
      "username": "dr_aisha",
      "full_name": "Dr. Aisha Rehman"
    },
    "profile_image": "https://example.com/image.jpg",
    "specialization": "Cardiology",
    "institution": "Amrita Institute of Medical Sciences",
    "role": "MBBS Student",
    "is_online": true,
    "last_seen": "2024-01-15T10:30:00Z"
  },
  "content": "Hello! How are you doing?",
  "message_type": "text",
  "media_url": null,
  "file_name": null,
  "file_size": null,
  "reply_to": null,
  "is_edited": false,
  "edited_at": null,
  "status": "read",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

## 🔧 **Setup & Installation**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run Migrations**
```bash
python manage.py makemigrations chat
python manage.py migrate
```

### **3. Create Superuser**
```bash
python manage.py createsuperuser
```

### **4. Add Dummy Data (Optional)**
```bash
python manage.py add_chat_dummy_data
```

### **5. Run Development Server**
```bash
python manage.py runserver
```

## 🔍 **Filtering & Search**

### **User Filtering**
```
GET /api/v1/chat/api/users/?role=MBBS Student
GET /api/v1/chat/api/users/?institution=AIIMS Delhi
GET /api/v1/chat/api/users/?specialization=Cardiology
GET /api/v1/chat/api/users/?is_verified=true
```

### **Message Search**
```
GET /api/v1/chat/api/messages/search/?q=cardiology
GET /api/v1/chat/api/messages/search/?room_id=uuid
GET /api/v1/chat/api/messages/search/?message_type=text
GET /api/v1/chat/api/messages/search/?date_from=2024-01-01
```

### **User Search**
```
GET /api/v1/chat/api/search/users/?q=dr_aisha
GET /api/v1/chat/api/search/users/?role=MBBS Student
GET /api/v1/chat/api/search/users/?institution=AIIMS
GET /api/v1/chat/api/search/users/?specialization=Cardiology
```

## 🔐 **Authentication**

All API endpoints require authentication. Use JWT tokens or session authentication:

```bash
# With JWT Token
curl -H "Authorization: Bearer <token>" \
     https://api.example.com/api/v1/chat/api/users/

# With Session
curl -H "Cookie: sessionid=<session_id>" \
     https://api.example.com/api/v1/chat/api/users/
```

## 📱 **Frontend Integration**

### **Example: Get User's Chat Rooms**
```javascript
const fetchUserRooms = async () => {
  const response = await fetch('/api/v1/chat/api/rooms/', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  return response.json();
};
```

### **Example: Send Message**
```javascript
const sendMessage = async (roomId, content) => {
  const response = await fetch(`/api/v1/chat/api/rooms/${roomId}/messages/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      content,
      message_type: 'text'
    })
  });
  return response.json();
};
```

### **Example: Add Contact**
```javascript
const addContact = async (contactId, nickname) => {
  const response = await fetch('/api/v1/chat/api/contacts/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      contact: contactId,
      nickname
    })
  });
  return response.json();
};
```

## 🧪 **Testing**

Run the test suite:
```bash
python manage.py test chat
```

## 📈 **Admin Interface**

Access the admin interface at `/admin/` to:
- Manage chat users and their verification status
- Moderate messages and rooms
- View message delivery statistics
- Manage contacts and notifications
- Monitor user activity and engagement

## 🚀 **Deployment Considerations**

### **Infrastructure**
- Django application server
- PostgreSQL database
- Redis for caching and WebSocket (future)
- Nginx reverse proxy
- WebSocket support (Django Channels - future)

### **Environment Variables**
```
DATABASE_URL=postgresql://...
REDIS_URL=redis://... (for future WebSocket)
JWT_SECRET_KEY=...
AWS_S3_BUCKET=... (for file uploads)
```

## 📞 **Support**

For API documentation and support:
- Check the Django admin interface for data management
- Use the test suite to verify functionality
- Review the models and serializers for data structure
- Check the signals for automatic notification handling

## 🔄 **Migration from Static**

The API is designed to replace the static JSON data in the frontend:

```javascript
// Old static approach
const contacts = await fetch('lib/screens/chat/data.json');

// New API approach
const contacts = await fetch('/api/v1/chat/api/users/?role=MBBS Student');
```

This provides real-time data, user interactions, and dynamic content management for the medical community platform! 🏥💬 