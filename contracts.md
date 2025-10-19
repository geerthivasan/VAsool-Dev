# Vasool Clone - Backend Integration Contracts

## API Endpoints

### Authentication APIs

#### 1. POST /api/auth/signup
**Request:**
```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```
**Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "user_id": "string"
}
```

#### 2. POST /api/auth/login
**Request:**
```json
{
  "email": "string",
  "password": "string"
}
```
**Response:**
```json
{
  "success": true,
  "token": "jwt_token",
  "user": {
    "id": "string",
    "name": "string",
    "email": "string"
  }
}
```

#### 3. GET /api/auth/me
**Headers:** Authorization: Bearer <token>
**Response:**
```json
{
  "id": "string",
  "name": "string",
  "email": "string"
}
```

### Chat/AI Assistant APIs

#### 4. POST /api/chat/message
**Headers:** Authorization: Bearer <token>
**Request:**
```json
{
  "message": "string",
  "session_id": "string" (optional)
}
```
**Response:**
```json
{
  "response": "string",
  "session_id": "string",
  "timestamp": "datetime"
}
```

#### 5. GET /api/chat/history
**Headers:** Authorization: Bearer <token>
**Query:** session_id (optional)
**Response:**
```json
{
  "messages": [
    {
      "id": "string",
      "sender": "user|assistant",
      "message": "string",
      "timestamp": "datetime"
    }
  ]
}
```

### Demo & Contact APIs

#### 6. POST /api/demo/schedule
**Request:**
```json
{
  "name": "string",
  "email": "string",
  "company": "string",
  "phone": "string"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Demo request received"
}
```

#### 7. POST /api/contact/sales
**Request:**
```json
{
  "name": "string",
  "email": "string",
  "message": "string"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Message sent successfully"
}
```

### Dashboard Analytics API

#### 8. GET /api/dashboard/analytics
**Headers:** Authorization: Bearer <token>
**Response:**
```json
{
  "total_outstanding": "number",
  "recovery_rate": "number",
  "active_accounts": "number",
  "recent_activity": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "timestamp": "datetime",
      "amount": "number" (optional)
    }
  ]
}
```

## MongoDB Collections

### 1. users
```javascript
{
  _id: ObjectId,
  name: String,
  email: String (unique, indexed),
  password: String (hashed),
  created_at: DateTime,
  updated_at: DateTime
}
```

### 2. chat_sessions
```javascript
{
  _id: ObjectId,
  user_id: ObjectId (ref: users),
  session_id: String (indexed),
  messages: [
    {
      sender: String ("user" | "assistant"),
      message: String,
      timestamp: DateTime
    }
  ],
  created_at: DateTime,
  updated_at: DateTime
}
```

### 3. demo_requests
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  company: String,
  phone: String,
  status: String ("pending" | "contacted" | "completed"),
  created_at: DateTime
}
```

### 4. contact_messages
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  message: String,
  status: String ("new" | "read" | "replied"),
  created_at: DateTime
}
```

## Mock Data to Replace in Frontend

### mockData.js
- **mockUser**: Will be replaced with actual authentication
- **mockChatMessages**: Will be fetched from backend API
- **mockTeamMembers**: Can remain static (no backend needed)
- **mockAgents**: Can remain static (no backend needed)

## Frontend Integration Changes

### Files to Update:

1. **Login.jsx**
   - Replace localStorage authentication with API call to `/api/auth/login`
   - Store JWT token in localStorage
   - Handle error responses properly

2. **Signup.jsx**
   - Replace mock signup with API call to `/api/auth/signup`
   - Redirect to login on success

3. **Dashboard.jsx**
   - Add authentication check using `/api/auth/me`
   - Replace mock chat messages with `/api/chat/history`
   - Replace mock AI responses with `/api/chat/message`
   - Fetch dashboard analytics from `/api/dashboard/analytics`

4. **Landing.jsx**
   - Connect Schedule Demo form to `/api/demo/schedule`
   - Connect Contact Sales form to `/api/contact/sales`

## Security Considerations
- All passwords will be hashed using bcrypt
- JWT tokens for authentication
- Protected routes require valid JWT token
- CORS properly configured
- Input validation on all endpoints

## Notes
- Chat AI responses will be mock responses for MVP (can integrate real LLM later)
- Dashboard analytics will show mock data initially (can connect to real data source later)
- Team members and agent details remain static on frontend
