# 🏗️ Cavity - Social Platform API

A comprehensive REST API for the Cavity social platform, designed for medical students and aspirants to share experiences, ask questions, and connect with peers.

## 📋 **Features**

- ✅ **User Management** - Registration, profiles, year-based filtering
- ✅ **Posts & Comments** - Create, read, update, delete with threading
- ✅ **Social Interactions** - Likes, shares, follows
- ✅ **Real-time Notifications** - Automatic notifications for interactions
- ✅ **Search & Filtering** - Search posts and users by various criteria
- ✅ **Admin Interface** - Comprehensive Django admin for content moderation

## 🗄️ **Database Models**

### **Core Models:**
- **User** - Custom user model with year tags and verification
- **Post** - User-generated content with media support
- **Comment** - Threaded comments with replies
- **PostLike/CommentLike** - Like/unlike functionality
- **PostShare** - Track sharing across platforms
- **Notification** - Real-time notifications
- **UserFollow** - User following relationships

## 🌐 **API Endpoints**

### **Authentication & Users**
```
GET    /api/v1/cavity/api/auth/profile/          # Get current user profile
PUT    /api/v1/cavity/api/auth/profile/          # Update profile
GET    /api/v1/cavity/api/users/                 # List users
GET    /api/v1/cavity/api/users/{id}/            # Get user details
GET    /api/v1/cavity/api/users/{id}/posts/      # Get user's posts
GET    /api/v1/cavity/api/users/{id}/likes/      # Get user's liked posts
POST   /api/v1/cavity/api/users/{id}/follow/     # Follow user
DELETE /api/v1/cavity/api/users/{id}/follow/     # Unfollow user
```

### **Posts**
```
GET    /api/v1/cavity/api/posts/                 # List posts (with filters)
POST   /api/v1/cavity/api/posts/                 # Create post
GET    /api/v1/cavity/api/posts/{id}/            # Get post details
PUT    /api/v1/cavity/api/posts/{id}/            # Update post
DELETE /api/v1/cavity/api/posts/{id}/            # Delete post
GET    /api/v1/cavity/api/posts/{id}/comments/   # Get post comments
GET    /api/v1/cavity/api/posts/{id}/likes/      # Get post likes
POST   /api/v1/cavity/api/posts/{id}/like/       # Like post
DELETE /api/v1/cavity/api/posts/{id}/like/       # Unlike post
POST   /api/v1/cavity/api/posts/{id}/share/      # Share post
```

### **Comments**
```
GET    /api/v1/cavity/api/comments/              # List comments
POST   /api/v1/cavity/api/comments/              # Create comment
GET    /api/v1/cavity/api/comments/{id}/         # Get comment details
PUT    /api/v1/cavity/api/comments/{id}/         # Update comment
DELETE /api/v1/cavity/api/comments/{id}/         # Delete comment
GET    /api/v1/cavity/api/comments/{id}/replies/ # Get comment replies
GET    /api/v1/cavity/api/comments/{id}/likes/   # Get comment likes
POST   /api/v1/cavity/api/comments/{id}/like/    # Like comment
DELETE /api/v1/cavity/api/comments/{id}/like/    # Unlike comment
```

### **Notifications**
```
GET    /api/v1/cavity/api/notifications/         # List notifications
PUT    /api/v1/cavity/api/notifications/{id}/read/ # Mark as read
PUT    /api/v1/cavity/api/notifications/read-all/ # Mark all as read
GET    /api/v1/cavity/api/notifications/unread-count/ # Get unread count
```

### **Search**
```
GET    /api/v1/cavity/api/search/posts/?q={query} # Search posts
GET    /api/v1/cavity/api/search/users/?q={query} # Search users
```

## 🔧 **Setup & Installation**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run Migrations**
```bash
python manage.py makemigrations cavity
python manage.py migrate
```

### **3. Create Superuser**
```bash
python manage.py createsuperuser
```

### **4. Add Dummy Data (Optional)**
```bash
python manage.py add_cavity_dummy_data
```

### **5. Run Development Server**
```bash
python manage.py runserver
```

## 📊 **API Response Examples**

### **User Response**
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
  "follower_count": 12,
  "following_count": 8,
  "post_count": 15,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### **Post Response**
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

## 🔍 **Filtering & Search**

### **Post Filtering**
```
GET /api/v1/cavity/api/posts/?year=3rd year MBBS
GET /api/v1/cavity/api/posts/?user=uuid
GET /api/v1/cavity/api/posts/?date=2024-01-15
GET /api/v1/cavity/api/posts/?search=cardiology
```

### **User Filtering**
```
GET /api/v1/cavity/api/users/?year_tag=NEET 2025
GET /api/v1/cavity/api/users/?is_verified=true
GET /api/v1/cavity/api/users/?search=dr_aisha
```

## 🔐 **Authentication**

All API endpoints require authentication. Use JWT tokens or session authentication:

```bash
# With JWT Token
curl -H "Authorization: Bearer <token>" \
     https://api.example.com/api/v1/cavity/api/posts/

# With Session
curl -H "Cookie: sessionid=<session_id>" \
     https://api.example.com/api/v1/cavity/api/posts/
```

## 📱 **Frontend Integration**

### **Example: Fetch Posts by Year**
```javascript
const fetchPostsByYear = async (year) => {
  const response = await fetch(`/api/v1/cavity/api/posts/?year=${year}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  return response.json();
};
```

### **Example: Create Post**
```javascript
const createPost = async (content, isAnonymous = false) => {
  const response = await fetch('/api/v1/cavity/api/posts/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      content,
      is_anonymous: isAnonymous
    })
  });
  return response.json();
};
```

## 🧪 **Testing**

Run the test suite:
```bash
python manage.py test cavity
```

## 📈 **Admin Interface**

Access the admin interface at `/admin/` to:
- Manage users and their verification status
- Moderate posts and comments
- View analytics and engagement metrics
- Manage notifications and follows

## 🚀 **Deployment**

### **Environment Variables**
```bash
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

### **Production Settings**
- Use PostgreSQL instead of SQLite
- Configure Redis for caching
- Set up proper CORS settings
- Enable HTTPS
- Configure media file storage

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
const posts = await fetch('assets/cavity_data.json');

// New API approach
const posts = await fetch('/api/v1/cavity/api/posts/?year=NEET 2025');
```

This provides real-time data, user interactions, and dynamic content management. 