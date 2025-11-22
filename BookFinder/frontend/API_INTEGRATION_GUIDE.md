# API Integration Guide

## ✅ What We've Done

### 1. **Created API Client** (`utils/api_client.py`)
- HTTP client for making requests to backend
- Error handling for network issues, timeouts, 404s, etc.
- User-friendly error messages in Streamlit
- Singleton pattern for efficient resource usage

### 2. **Added Configuration** (`config/settings.py`)
- Backend URL configuration (currently set to `http://localhost:8000`)
- API endpoint paths
- Timeout settings
- Mock data fallback toggle

### 3. **Data Transformation Layer** (`utils/transformers.py`)
- Converts backend API format to frontend format
- Handles missing fields gracefully
- Maps multiple stores to single store + stores array
- Default values for missing data (ratings, prices)

### 4. **Updated Search** (`utils/search.py`)
- Replaced mock search with real API calls
- Fallback to mock data if API fails (configurable)
- Loading spinner while searching
- Handles empty results

---

## 🔧 How to Use

### **Step 1: Update Backend URL**

In `config/settings.py`, change:

```python
BACKEND_URL = "http://localhost:8000"  # Your backend URL here
```

### **Step 2: Start Your Backend**

Make sure your backend is running at the configured URL.

### **Step 3: Run the Frontend**

```bash
cd /Users/ani.a.harutyunyan/Documents/AUA/group-2/BookFinder/frontend
source ../../venv/bin/activate
streamlit run app_refactored.py
```

### **Step 4: Test Search**

1. Open the app in your browser
2. Type a search query (e.g., "anna", "tolstoy", "rose")
3. The app will call `/api/books/search?search_query=your_query`
4. Results will be displayed in cards

---

## 📊 API Response Mapping

### Backend Response → Frontend Format

```python
# Backend gives:
{
    "bookId": "abc123",
    "title": "Anna Karenina",
    "author": "Leo Tolstoy",
    "description": "A tragic love story...",
    "genre": "Classic Literature",
    "language": "English",
    "isbn": "978-0-14-303500-8",
    "stores": [
        {
            "storeName": "Bookinist",
            "address": "123 Main St",
            "phone": "+374 10 123456"
        }
    ]
}

# We transform to:
{
    "id": "abc123",
    "title": "Anna Karenina",
    "author": "Leo Tolstoy",
    "description": "A tragic love story..." (first 200 chars),
    "long_description": "A tragic love story..." (full text),
    "rating": 4.0,  # Default, will be updated from ratings API
    "genre": "Classic Literature",
    "language": "English",
    "isbn": "978-0-14-303500-8",
    "store": {  # Primary store (first one)
        "name": "Bookinist",
        "price": 0,  # Not in API yet
        "currency": "AMD",
        "address": "123 Main St",
        "phone": "+374 10 123456"
    },
    "stores": [...]  # All stores
}
```

---

## ⚙️ Configuration Options

### `config/settings.py`

```python
# Backend URL - change this based on environment
BACKEND_URL = "http://localhost:8000"  # Local dev
# BACKEND_URL = "https://your-backend.com"  # Production

# Use mock data if API fails?
USE_MOCK_FALLBACK = True  # True = show mock data on error
                          # False = show error message only

# Request timeout
API_TIMEOUT = 10  # seconds
```

---

## 🐛 Troubleshooting

### **Error: "Cannot connect to backend"**

**Problem**: Frontend can't reach backend  
**Solutions**:
1. Check if backend is running (`docker-compose up` or similar)
2. Verify `BACKEND_URL` in `config/settings.py`
3. Check firewall/network settings
4. If using Docker, ensure containers can communicate

### **Error: "Request timeout"**

**Problem**: Backend is slow/unresponsive  
**Solutions**:
1. Increase `API_TIMEOUT` in settings
2. Check backend logs for errors
3. Check database connectivity
4. Optimize backend queries

### **Empty Results**

**Problem**: Search returns no books  
**Solutions**:
1. Check if backend database has data
2. Verify search query format
3. Check backend logs for errors
4. Test backend API directly (curl or Postman)

### **CORS Errors** (if you see them in browser console)

**Problem**: Backend blocking frontend requests  
**Solution**: Add CORS middleware to backend:

```python
# In your FastAPI backend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

##  Next Steps (Optional Enhancements)

### **1. Add Ratings Integration**

Currently, ratings are hardcoded. To integrate:

1. Call `GET /api/ratings/{book_id}` in `render_detail()`
2. Display actual rating
3. Add UI for users to rate (star selector)
4. Call `POST /api/ratings/` on submit

### **2. Add Authentication**

1. Create login component
2. Implement Google OAuth flow
3. Store token in session
4. Include token in API requests

### **3. Add Caching**

Reduce API calls by caching results:

```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def search_books_cached(query):
    return simple_search(query)
```

### **4. Add Pagination**

If backend supports it:
- Add page/limit params to search
- Add "Load More" button
- Show results count

### **5. Better Error Handling**

- Retry failed requests
- Show specific error messages
- Log errors for debugging

---

## 📝 Testing Checklist

Before deployment, test:

- [ ] Search with valid query returns results
- [ ] Search with no matches shows appropriate message
- [ ] Backend down shows error + fallback (if enabled)
- [ ] Click "View" button navigates to detail page
- [ ] Detail page shows all book info correctly
- [ ] Back button returns to results
- [ ] Multiple stores display correctly
- [ ] Page loads without errors in console
- [ ] Responsive on mobile devices

---

## 🚀 Deployment Notes

### **Environment Variables**

For production, use environment variables instead of hardcoded URLs:

```python
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
```

Then set in your deployment platform:
```bash
export BACKEND_URL=https://your-backend.com
```

### **Docker**

If using Docker Compose, both services should be in same network:

```yaml
services:
  backend:
    ...
    networks:
      - app-network
  
  frontend:
    ...
    environment:
      - BACKEND_URL=http://backend:8000
    networks:
      - app-network

networks:
  app-network:
```

---

## 💡 Quick Tips

1. **Development**: Keep `USE_MOCK_FALLBACK = True` to keep working if backend crashes
2. **Production**: Set `USE_MOCK_FALLBACK = False` to catch real errors
3. **Debugging**: Check browser Network tab to see actual API requests
4. **Performance**: Add caching for frequently accessed data
5. **Testing**: Use tools like Postman to test backend independently

---

## 📞 Need Help?

If something isn't working:

1. Check backend logs
2. Check Streamlit terminal output
3. Check browser console (F12)
4. Test API with curl:
   ```bash
   curl "http://localhost:8000/api/books/search?search_query=anna"
   ```
5. Enable debug mode in Streamlit (verbose errors)

---

**Happy Coding! 🎉**
