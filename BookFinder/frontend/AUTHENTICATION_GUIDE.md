# Google OAuth Authentication Integration Guide

## 🎯 Overview
Complete Google OAuth integration for the BookFinder application, allowing users to log in and rate books.

## 📋 What Was Implemented

### 1. **Backend Changes** (`backend/app/routers/auth.py`)
- Modified `/api/auth/google/callback` to redirect to frontend with token
- Returns JWT token, email, and name in URL parameters
- Token expires in 24 hours

### 2. **Frontend Components**

#### **New Login Page** (`components/login.py`)
- Dedicated `/login` view for authentication
- Beautiful UI with Google OAuth button
- Shows welcome message if already logged in
- Explains benefits of logging in

#### **Auth Management** (`components/auth.py`)
- Sidebar auth widget
- Shows user info when logged in
- Logout button
- "Go to Login" button when not authenticated

#### **Updated Rating Widget** (`components/rating_widget.py`)
- Requires authentication to submit ratings
- Shows "Go to Login Page" button if not logged in
- Displays user email when rating
- Sends JWT token with rating requests

#### **Session Management** (`utils/session.py`)
- `login(token, email, name)` - Store auth credentials
- `logout()` - Clear auth state
- `is_authenticated()` - Check auth status
- `get_auth_token()` - Retrieve JWT token
- `get_user_info()` - Get email/name
- `go_to_login()` - Navigate to login page

#### **API Client** (`utils/api_client.py`)
- Accepts `auth_token` parameter
- Sets `Authorization: Bearer <token>` header
- Singleton pattern with token management
- Better error handling for 401 Unauthorized

#### **Main App** (`app.py`)
- Handles OAuth callback from Google
- Extracts token from URL parameters
- Stores credentials in session
- Shows auth status in header
- Added `/login` route

## 🔄 Authentication Flow

```
1. User clicks "Login" → Goes to /login page
2. User clicks "Continue with Google" → Redirects to backend /api/auth/google
3. Backend redirects to Google OAuth
4. User authenticates with Google
5. Google redirects back to /api/auth/google/callback
6. Backend creates JWT token
7. Backend redirects to frontend: http://localhost:8501?token=XXX&email=user@example.com&name=User
8. Frontend extracts token from URL
9. Frontend stores token in session
10. User can now rate books (token sent in Authorization header)
```

## 🧪 Testing Instructions

### Test Authentication:
1. Start backend: `cd backend && uvicorn app.main:app --reload --port 8000`
2. Start frontend: `cd frontend && streamlit run app.py`
3. Click "🔑 Login" button in header
4. Click "Continue with Google" on login page
5. Authenticate with Google
6. Should redirect back with token
7. Should see your name/email in header

### Test Rating Submission:
1. Login (follow above steps)
2. Search for a book
3. Click "View" on a book
4. Scroll to "Rate This Book" tab
5. Select stars and add comment
6. Click "Submit Rating"
7. Should see success message
8. Check backend database for new rating

### Test Logout:
1. While logged in, open sidebar
2. Click "🚪 Logout"
3. Should clear session
4. Try to rate a book → Should see "Go to Login Page" button

## 🔧 Configuration

### Backend `.env`:
```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
API_SECRET_KEY=your_jwt_secret_key
```

### Frontend - No config needed!
Uses environment variable `BACKEND_URL` (defaults to `http://localhost:8000`)

## 🐛 Troubleshooting

### Issue: "Server error: 401" when rating
**Solution:** User is not logged in. Click "Go to Login Page" button.

### Issue: OAuth redirect doesn't work
**Solution:** Check that Google OAuth credentials are configured in backend `.env`

### Issue: Token not saved after redirect
**Solution:** Clear browser cache and try again. Check browser console for errors.

### Issue: "Cannot connect to backend"
**Solution:** 
- Local dev: Backend should be at `http://localhost:8000`
- Docker: Backend should be at `http://backend:8000`

## 📁 Files Changed

### Backend:
- `app/routers/auth.py` - Modified callback to redirect with token

### Frontend:
- `app.py` - Added auth callback handler and login route
- `components/login.py` - NEW: Dedicated login page
- `components/auth.py` - Sidebar auth widget
- `components/rating_widget.py` - Protected rating submission
- `utils/session.py` - Auth state management functions
- `utils/api_client.py` - JWT token handling
- `config/settings.py` - Already had auth endpoints

## 🎨 UI Features

- **Header**: Shows user name/email or Login button
- **Sidebar**: Full auth details with logout
- **Login Page**: Beautiful centered card with Google button
- **Rating Form**: Shows user email, requires login
- **Protected Routes**: Automatically redirects to login if needed

## 🔐 Security Notes

- JWT tokens expire in 24 hours
- Tokens stored in Streamlit session (memory only)
- Uses secure Google OAuth flow
- Backend validates all JWT tokens
- Never stores passwords

## ✅ Success Criteria

- ✅ Users can login with Google
- ✅ JWT token properly stored in session
- ✅ Token sent with rating requests
- ✅ Backend validates token and extracts user email
- ✅ Ratings tied to authenticated user
- ✅ Users can logout
- ✅ Nice UI/UX for login flow

## 🚀 Next Steps (Optional)

1. Add remember me / persistent storage
2. Add profile page
3. Add user's rating history
4. Add social features (follow users, etc.)
5. Add admin dashboard
6. Add role-based permissions

---

**Authentication integration complete!** 🎉
