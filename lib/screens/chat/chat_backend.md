# 💬 Chat System - REST API Planning Document

## 📋 **Overview**
This document outlines the REST API architecture needed to convert the Chat screen from static JSON data to a dynamic, real-time messaging platform for medical students and professionals.

---

## 🎯 **Core Functionality Analysis**

### **Current Static Features:**
- ✅ Contact list with medical professionals
- ✅ Search functionality (name, role, institution)
- ✅ Add contact functionality (UI only)
- ✅ Contact cards with profile images
- ✅ Role-based filtering (MBBS Student, Intern, GP, etc.)
- ✅ Institution-based organization

### **Required Dynamic Features:**
- 🔄 Real-time messaging between users
- 🔄 Contact management (add/remove contacts)
- 🔄 Online/offline status
- 🔄 Message history and persistence
- 🔄 Push notifications for new messages
- 🔄 File/media sharing in chats
- 🔄 Message status (sent, delivered, read)
- 🔄 Group chat functionality
- 🔄 Message search and filtering

---

## 🗄️ **Database Schema Design**

### **1. ChatUser Table (extends User)**
```sql
chat_users (
  id: UUID (Primary Key, inherits from User)
  user_id: UUID (Foreign Key -> users.id)
  is_online: BOOLEAN DEFAULT FALSE
  last_seen: TIMESTAMP
  profile_image: VARCHAR(255) -- URL to image
  bio: TEXT
  specialization: VARCHAR(100) -- Medical specialization
  institution: VARCHAR(200)
  role: VARCHAR(100) -- MBBS Student, Intern, GP, etc.
  is_verified: BOOLEAN DEFAULT FALSE
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
)
```

### **2. ChatRoom Table**
```sql
chat_rooms (
  id: UUID (Primary Key)
  name: VARCHAR(200) -- For group chats
  type: ENUM('direct', 'group') DEFAULT 'direct'
  created_by: UUID (Foreign Key -> chat_users.id)
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
)
```

### **3. ChatRoomParticipant Table**
```sql
chat_room_participants (
  id: UUID (Primary Key)
  room_id: UUID (Foreign Key -> chat_rooms.id)
  user_id: UUID (Foreign Key -> chat_users.id)
  role: ENUM('admin', 'member') DEFAULT 'member'
  joined_at: TIMESTAMP
  left_at: TIMESTAMP NULL
  is_active: BOOLEAN DEFAULT TRUE
)
```

### **4. Message Table**
```sql
messages (
  id: UUID (Primary Key)
  room_id: UUID (Foreign Key -> chat_rooms.id)
  sender_id: UUID (Foreign Key -> chat_users.id)
  content: TEXT
  message_type: ENUM('text', 'image', 'file', 'audio', 'video') DEFAULT 'text'
  media_url: VARCHAR(500) NULL
  file_name: VARCHAR(200) NULL
  file_size: INTEGER NULL
  reply_to: UUID (Foreign Key -> messages.id) NULL -- For reply messages
  is_edited: BOOLEAN DEFAULT FALSE
  edited_at: TIMESTAMP NULL
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
)
```

### **5. MessageStatus Table**
```sql
message_status (
  id: UUID (Primary Key)
  message_id: UUID (Foreign Key -> messages.id)
  user_id: UUID (Foreign Key -> chat_users.id)
  status: ENUM('sent', 'delivered', 'read') DEFAULT 'sent'
  updated_at: TIMESTAMP
)
```

### **6. Contact Table**
```sql
contacts (
  id: UUID (Primary Key)
  user_id: UUID (Foreign Key -> chat_users.id)
  contact_id: UUID (Foreign Key -> chat_users.id)
  nickname: VARCHAR(100) NULL
  is_favorite: BOOLEAN DEFAULT FALSE
  is_blocked: BOOLEAN DEFAULT FALSE
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
  UNIQUE(user_id, contact_id)
)
```

### **7. ChatNotification Table**
```sql
chat_notifications (
  id: UUID (Primary Key)
  user_id: UUID (Foreign Key -> chat_users.id)
  message_id: UUID (Foreign Key -> messages.id)
  type: ENUM('new_message', 'message_reply', 'contact_request', 'group_invite')
  is_read: BOOLEAN DEFAULT FALSE
  created_at: TIMESTAMP
)
```

---

## 🌐 **REST API Endpoints**

### **🔐 Authentication & User Management**
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/refresh
GET    /api/auth/profile
PUT    /api/auth/profile
POST   /api/auth/forgot-password
POST   /api/auth/reset-password
```

### **👥 Chat User Management**
```
GET    /api/chat/users
GET    /api/chat/users/{id}
PUT    /api/chat/users/{id}
GET    /api/chat/users/{id}/status
PUT    /api/chat/users/{id}/status
GET    /api/chat/users/search?q={query}
GET    /api/chat/users/filter?role={role}&institution={institution}
```

### **📞 Contact Management**
```
GET    /api/chat/contacts
POST   /api/chat/contacts
GET    /api/chat/contacts/{id}
PUT    /api/chat/contacts/{id}
DELETE /api/chat/contacts/{id}
POST   /api/chat/contacts/{id}/favorite
DELETE /api/chat/contacts/{id}/favorite
POST   /api/chat/contacts/{id}/block
DELETE /api/chat/contacts/{id}/block
```

### **💬 Chat Rooms**
```
GET    /api/chat/rooms
POST   /api/chat/rooms
GET    /api/chat/rooms/{id}
PUT    /api/chat/rooms/{id}
DELETE /api/chat/rooms/{id}
GET    /api/chat/rooms/{id}/participants
POST   /api/chat/rooms/{id}/participants
DELETE /api/chat/rooms/{id}/participants/{user_id}
```

### **💭 Messages**
```
GET    /api/chat/rooms/{room_id}/messages
POST   /api/chat/rooms/{room_id}/messages
GET    /api/chat/rooms/{room_id}/messages/{id}
PUT    /api/chat/rooms/{room_id}/messages/{id}
DELETE /api/chat/rooms/{room_id}/messages/{id}
POST   /api/chat/rooms/{room_id}/messages/{id}/reply
GET    /api/chat/rooms/{room_id}/messages/search?q={query}
```

### **📊 Message Status**
```
GET    /api/chat/messages/{id}/status
PUT    /api/chat/messages/{id}/status
POST   /api/chat/messages/{id}/mark-read
POST   /api/chat/rooms/{room_id}/mark-all-read
```

### **🔔 Notifications**
```
GET    /api/chat/notifications
PUT    /api/chat/notifications/{id}/read
PUT    /api/chat/notifications/read-all
DELETE /api/chat/notifications/{id}
GET    /api/chat/notifications/unread-count
```

### **📁 File Upload**
```
POST   /api/chat/upload/image
POST   /api/chat/upload/file
POST   /api/chat/upload/audio
POST   /api/chat/upload/video
DELETE /api/chat/upload/{file_id}
```

---

## 📊 **API Response Models**

### **ChatUser Model**
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

### **ChatRoom Model**
```json
{
  "id": "uuid",
  "name": "Direct Chat",
  "type": "direct",
  "created_by": "uuid",
  "participants": [
    {
      "id": "uuid",
      "user": {
        "id": "uuid",
        "username": "dr_aisha",
        "full_name": "Dr. Aisha Rehman",
        "profile_image": "https://example.com/image.jpg"
      },
      "role": "member",
      "is_online": true,
      "last_seen": "2024-01-15T10:30:00Z"
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

### **Message Model**
```json
{
  "id": "uuid",
  "room_id": "uuid",
  "sender": {
    "id": "uuid",
    "username": "dr_aisha",
    "full_name": "Dr. Aisha Rehman",
    "profile_image": "https://example.com/image.jpg"
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

### **Contact Model**
```json
{
  "id": "uuid",
  "contact": {
    "id": "uuid",
    "username": "dr_aisha",
    "full_name": "Dr. Aisha Rehman",
    "profile_image": "https://example.com/image.jpg",
    "specialization": "Cardiology",
    "institution": "Amrita Institute of Medical Sciences",
    "role": "MBBS Student",
    "is_online": true,
    "last_seen": "2024-01-15T10:30:00Z"
  },
  "nickname": "Aisha",
  "is_favorite": true,
  "is_blocked": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

## 🔧 **Implementation Phases**

### **Phase 1: Core Infrastructure** 🚀
- [ ] Set up Django REST Framework backend
- [ ] Implement user authentication (JWT tokens)
- [ ] Create database models and migrations
- [ ] Set up basic CRUD operations for chat users
- [ ] Implement contact management system

### **Phase 2: Messaging Features** 💬
- [ ] Add chat room creation and management
- [ ] Implement message sending and receiving
- [ ] Add message status tracking (sent, delivered, read)
- [ ] Create real-time messaging (WebSocket)
- [ ] Add message search and filtering

### **Phase 3: Advanced Features** 🔍
- [ ] Add file/media sharing
- [ ] Implement group chat functionality
- [ ] Add push notifications
- [ ] Create message reply system
- [ ] Add message editing and deletion

### **Phase 4: Real-time & Optimization** ⚡
- [ ] Implement WebSocket connections
- [ ] Add online/offline status
- [ ] Implement message caching
- [ ] Add rate limiting
- [ ] Optimize for large message volumes

---

## 🔐 **Security Considerations**

### **Authentication & Authorization**
- JWT token-based authentication
- Role-based access control
- Message encryption (optional)
- File upload security

### **Data Protection**
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- File type validation for uploads

### **Privacy & Compliance**
- Message retention policies
- GDPR compliance for user data
- Contact blocking functionality
- Message deletion capabilities

---

## 📱 **Frontend Integration Points**

### **Current Static Features → Dynamic API Calls**
```
❌ Static JSON loading
✅ GET /api/chat/users?role=MBBS Student

❌ Hardcoded contact data
✅ GET /api/chat/contacts

❌ Mock add contact
✅ POST /api/chat/contacts

❌ No real-time updates
✅ WebSocket connection for live messaging
```

### **New Dynamic Features**
```
🆕 Real-time messaging
🆕 Contact management
🆕 Online/offline status
🆕 Message history
🆕 Push notifications
🆕 File sharing
🆕 Group chats
🆕 Message search
```

---

## 🧪 **Testing Strategy**

### **Unit Tests**
- Model validation tests
- API endpoint tests
- Authentication tests
- Message encryption tests

### **Integration Tests**
- End-to-end messaging workflows
- File upload/download tests
- Real-time communication tests
- Contact management tests

### **Performance Tests**
- Load testing for concurrent users
- Message delivery performance
- File upload/download speeds
- Database query optimization

---

## 📈 **Monitoring & Analytics**

### **Key Metrics**
- Active chat users per day
- Messages sent per day
- File upload/download rates
- User engagement rates
- API response times

### **Error Tracking**
- Message delivery failures
- File upload errors
- WebSocket connection issues
- API error rates

---

## 🚀 **Deployment Considerations**

### **Infrastructure**
- Django application server
- PostgreSQL database
- Redis for caching and WebSocket
- Nginx reverse proxy
- WebSocket support (Django Channels)

### **Environment Variables**
```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
JWT_SECRET_KEY=...
AWS_S3_BUCKET=... (for file uploads)
```

### **CI/CD Pipeline**
- Automated testing
- Code quality checks
- Database migrations
- Blue-green deployment

---

## 📋 **API Documentation**

### **Swagger/OpenAPI**
- Auto-generated API documentation
- Interactive testing interface
- Request/response examples
- Authentication documentation

### **Postman Collections**
- Pre-configured API requests
- Environment variables
- Test scripts
- Documentation export

---

## 🎯 **Success Metrics**

### **Technical Metrics**
- API response time < 100ms
- 99.9% uptime
- < 1% message delivery failure rate
- Support for 10,000+ concurrent users

### **User Experience Metrics**
- < 1 second message delivery
- Smooth real-time updates
- Intuitive contact management
- High user engagement rates

---

## 🔄 **Migration Strategy**

### **Phase 1: Parallel Development**
- Keep static JSON as fallback
- Implement API alongside existing code
- Gradual feature migration

### **Phase 2: Feature Parity**
- Ensure all static features work via API
- Maintain same UI/UX experience
- Add new dynamic features

### **Phase 3: Full Migration**
- Remove static JSON dependencies
- Optimize for dynamic data
- Add advanced features

---

## 💡 **Additional Features**

### **Medical-Specific Features**
- **Specialization-based filtering** - Filter contacts by medical specialization
- **Institution-based grouping** - Group contacts by medical institution
- **Role-based permissions** - Different access levels for students vs professionals
- **Medical case sharing** - Share medical cases with proper privacy controls
- **Study group chats** - Create study groups for medical students

### **Advanced Messaging**
- **Voice messages** - Send and receive voice messages
- **Medical image sharing** - Share X-rays, scans with annotations
- **Document sharing** - Share medical documents and notes
- **Message reactions** - React to messages with emojis
- **Message forwarding** - Forward messages to other contacts

### **Privacy & Security**
- **End-to-end encryption** - Secure message encryption
- **Message self-destruct** - Auto-delete messages after time
- **Contact verification** - Verify medical professional credentials
- **HIPAA compliance** - Ensure medical data privacy
- **Audit trails** - Track message access and modifications

---

This API planning document provides a comprehensive roadmap for converting the Chat screen from static to dynamic mode while maintaining all existing functionality and adding powerful new features for a better user experience in the medical community platform! 🏥💬
