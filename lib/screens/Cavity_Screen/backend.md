# 🏗️ Cavity Screen - REST API Planning Document

## 📋 **Overview**
This document outlines the REST API architecture needed to convert the Cavity screen from static JSON data to a dynamic, real-time social platform for medical students and aspirants.

---

## 🎯 **Core Functionality Analysis**

### **Current Static Features:**
- ✅ User posts with content, timestamps, and year tags
- ✅ Year-based filtering (NEET 2025, MBBS years, etc.)
- ✅ Like/Comment/Share interactions (UI only)
- ✅ User profiles with year identification
- ✅ Post sorting by timestamp

### **Required Dynamic Features:**
- 🔄 Real-time post creation and updates
- 🔄 User authentication and authorization
- 🔄 Interactive likes, comments, and shares
- 🔄 Real-time notifications
- 🔄 User profile management
- 🔄 Content moderation and reporting

---

## 🗄️ **Database Schema Design**

### **1. Users Table**
```sql
users (
  id: UUID (Primary Key)
  username: VARCHAR(50) UNIQUE
  email: VARCHAR(100) UNIQUE
  full_name: VARCHAR(100)
  year_tag: VARCHAR(50) -- NEET 2025, 1st year MBBS, etc.
  profile_image: VARCHAR(255) -- URL to image
  bio: TEXT
  is_verified: BOOLEAN DEFAULT FALSE
  is_active: BOOLEAN DEFAULT TRUE
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
)
```

### **2. Posts Table**
```sql
posts (
  id: UUID (Primary Key)
  user_id: UUID (Foreign Key -> users.id)
  content: TEXT
  media_urls: JSON -- Array of media URLs
  is_anonymous: BOOLEAN DEFAULT FALSE
  is_edited: BOOLEAN DEFAULT FALSE
  edit_history: JSON -- Track edit history
  status: ENUM('active', 'hidden', 'deleted') DEFAULT 'active'
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
)
```

### **3. Likes Table**
```sql
post_likes (
  id: UUID (Primary Key)
  post_id: UUID (Foreign Key -> posts.id)
  user_id: UUID (Foreign Key -> users.id)
  created_at: TIMESTAMP
  UNIQUE(post_id, user_id)
)
```

### **4. Comments Table**
```sql
comments (
  id: UUID (Primary Key)
  post_id: UUID (Foreign Key -> posts.id)
  user_id: UUID (Foreign Key -> users.id)
  parent_comment_id: UUID (Foreign Key -> comments.id) -- For nested replies
  content: TEXT
  is_edited: BOOLEAN DEFAULT FALSE
  status: ENUM('active', 'hidden', 'deleted') DEFAULT 'active'
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
)
```

### **5. Shares Table**
```sql
post_shares (
  id: UUID (Primary Key)
  post_id: UUID (Foreign Key -> posts.id)
  user_id: UUID (Foreign Key -> users.id)
  platform: VARCHAR(50) -- LinkedIn, WhatsApp, etc.
  shared_at: TIMESTAMP
)
```

### **6. Notifications Table**
```sql
notifications (
  id: UUID (Primary Key)
  user_id: UUID (Foreign Key -> users.id)
  type: ENUM('like', 'comment', 'share', 'mention', 'system')
  reference_id: UUID -- Post or comment ID
  reference_type: VARCHAR(50) -- 'post' or 'comment'
  message: TEXT
  is_read: BOOLEAN DEFAULT FALSE
  created_at: TIMESTAMP
)
```

---

## 🌐 **REST API Endpoints**

### **🔐 Authentication Endpoints**
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

### **👥 User Management**
```
GET    /api/users
GET    /api/users/{id}
PUT    /api/users/{id}
DELETE /api/users/{id}
GET    /api/users/{id}/posts
GET    /api/users/{id}/likes
POST   /api/users/{id}/follow
DELETE /api/users/{id}/follow
```

### **📝 Posts Management**
```
GET    /api/posts
POST   /api/posts
GET    /api/posts/{id}
PUT    /api/posts/{id}
DELETE /api/posts/{id}
GET    /api/posts/{id}/comments
GET    /api/posts/{id}/likes
```

### **💬 Comments Management**
```
GET    /api/comments
POST   /api/comments
GET    /api/comments/{id}
PUT    /api/comments/{id}
DELETE /api/comments/{id}
GET    /api/comments/{id}/replies
```

### **❤️ Interactions**
```
POST   /api/posts/{id}/like
DELETE /api/posts/{id}/like
POST   /api/posts/{id}/share
POST   /api/comments/{id}/like
DELETE /api/comments/{id}/like
```

### **🔔 Notifications**
```
GET    /api/notifications
PUT    /api/notifications/{id}/read
PUT    /api/notifications/read-all
DELETE /api/notifications/{id}
```

### **🔍 Search & Filtering**
```
GET    /api/posts/search?q={query}
GET    /api/posts/filter?year={year}&user={user_id}&date={date}
GET    /api/users/search?q={query}
```

---

## 📊 **API Response Models**

### **User Model**
```json
{
  "id": "uuid",
  "username": "dr_aisha",
  "email": "aisha@example.com",
  "full_name": "Dr. Aisha Rehman",
  "year_tag": "3rd year MBBS",
  "profile_image": "https://example.com/image.jpg",
  "bio": "Medical student passionate about cardiology",
  "is_verified": true,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### **Post Model**
```json
{
  "id": "uuid",
  "user": {
    "id": "uuid",
    "username": "dr_aisha",
    "full_name": "Dr. Aisha Rehman",
    "year_tag": "3rd year MBBS",
    "profile_image": "https://example.com/image.jpg"
  },
  "content": "Just finished my cardiology rotation! The ECG interpretation was challenging but fascinating...",
  "media_urls": ["https://example.com/image1.jpg"],
  "is_anonymous": false,
  "is_edited": false,
  "like_count": 12,
  "comment_count": 5,
  "share_count": 3,
  "is_liked_by_user": true,
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### **Comment Model**
```json
{
  "id": "uuid",
  "post_id": "uuid",
  "user": {
    "id": "uuid",
    "username": "med_student",
    "full_name": "John Doe",
    "year_tag": "2nd year MBBS",
    "profile_image": "https://example.com/image.jpg"
  },
  "content": "Great experience! Which ECG findings did you find most interesting?",
  "parent_comment_id": null,
  "like_count": 3,
  "is_liked_by_user": false,
  "replies_count": 2,
  "status": "active",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

---

## 🔧 **Implementation Phases**

### **Phase 1: Core Infrastructure** 🚀
- [ ] Set up Django REST Framework backend
- [ ] Implement user authentication (JWT tokens)
- [ ] Create database models and migrations
- [ ] Set up basic CRUD operations for posts
- [ ] Implement year-based filtering

### **Phase 2: Social Features** 💬
- [ ] Add like/unlike functionality
- [ ] Implement comment system
- [ ] Add share tracking
- [ ] Create notification system
- [ ] Implement real-time updates (WebSocket)

### **Phase 3: Advanced Features** 🔍
- [ ] Add search functionality
- [ ] Implement content moderation
- [ ] Add user profiles and following
- [ ] Create reporting system
- [ ] Add media upload support

### **Phase 4: Optimization** ⚡
- [ ] Implement caching (Redis)
- [ ] Add pagination for large datasets
- [ ] Optimize database queries
- [ ] Add rate limiting
- [ ] Implement analytics tracking

---

## 🔐 **Security Considerations**

### **Authentication & Authorization**
- JWT token-based authentication
- Role-based access control (User, Moderator, Admin)
- Token refresh mechanism
- Password hashing with bcrypt

### **Data Protection**
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting on sensitive endpoints

### **Content Moderation**
- Automated content filtering
- User reporting system
- Manual moderation tools
- Appeal process for removed content

---

## 📱 **Frontend Integration Points**

### **Current Static Features → Dynamic API Calls**
```
❌ Static JSON loading
✅ GET /api/posts?year={selectedYear}

❌ Hardcoded user data
✅ GET /api/users/{id}

❌ Mock interactions
✅ POST /api/posts/{id}/like

❌ Static comments
✅ GET /api/posts/{id}/comments

❌ No real-time updates
✅ WebSocket connection for live updates
```

### **New Dynamic Features**
```
🆕 Real-time notifications
🆕 User authentication
🆕 Post creation and editing
🆕 Comment threading
🆕 User profiles and following
🆕 Content search and filtering
🆕 Media upload support
```

---

## 🧪 **Testing Strategy**

### **Unit Tests**
- Model validation tests
- API endpoint tests
- Authentication tests
- Permission tests

### **Integration Tests**
- End-to-end API workflows
- Database transaction tests
- Third-party service integration

### **Performance Tests**
- Load testing for concurrent users
- Database query optimization
- API response time benchmarks

---

## 📈 **Monitoring & Analytics**

### **Key Metrics**
- Active users per day/week
- Posts created per day
- Engagement rates (likes, comments, shares)
- User retention rates
- API response times

### **Error Tracking**
- API error rates
- Database performance
- User-reported issues
- System health monitoring

---

## 🚀 **Deployment Considerations**

### **Infrastructure**
- Django application server
- PostgreSQL database
- Redis for caching
- Nginx reverse proxy
- WebSocket support (Django Channels)

### **Environment Variables**
```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
JWT_SECRET_KEY=...
AWS_S3_BUCKET=...
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
- API response time < 200ms
- 99.9% uptime
- < 1% error rate
- Support for 10,000+ concurrent users

### **User Experience Metrics**
- < 2 second page load time
- Smooth real-time updates
- Intuitive interaction patterns
- High engagement rates

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

This API planning document provides a comprehensive roadmap for converting the Cavity screen from static to dynamic mode while maintaining all existing functionality and adding powerful new features for a better user experience.
