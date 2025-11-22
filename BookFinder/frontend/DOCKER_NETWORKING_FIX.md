# Docker Networking Fix Guide

## 🐛 The Problem

When running in Docker Compose, containers **cannot** use `localhost` to communicate with each other.

### Why?
- `localhost` inside a container refers to **that container itself**
- Each container has its own network namespace
- Containers need to use **service names** to communicate

## ✅ The Solution

### **Docker Compose (Production)**
Use the **service name** as the hostname:
```yaml
environment:
  BACKEND_URL: "http://backend:8000"  # ✅ Correct - uses service name
  # NOT: "http://localhost:8000"      # ❌ Wrong - refers to container itself
```

### **Local Development (Without Docker)**
Use `localhost`:
```bash
# Running on your machine directly
BACKEND_URL="http://localhost:8008"  # ✅ Correct for local dev
```

---

## 📋 Quick Reference

| Scenario | Backend URL | Notes |
|----------|-------------|-------|
| **Docker Compose** | `http://backend:8000` | Use service name + internal port |
| **Local Dev (both running locally)** | `http://localhost:8008` | Use localhost + external port |
| **Frontend local, Backend in Docker** | `http://localhost:8008` | Use localhost + external port |
| **Production/Deployed** | `https://your-backend.com` | Use actual domain |

---

## 🔧 How It Works Now

### **1. docker-compose.yml**
```yaml
services:
  frontend:
    environment:
      BACKEND_URL: "http://backend:8000"  # Service name + internal port
  
  backend:
    ports:
      - "8008:8000"  # External:Internal
    # Inside Docker network: accessible as "backend:8000"
    # From host machine: accessible as "localhost:8008"
```

### **2. config/settings.py**
```python
import os

# Reads from environment variable (Docker)
# Falls back to localhost (local dev)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
```

---

## 🚀 How to Run

### **Option 1: Docker Compose (Recommended)**

```bash
cd /Users/ani.a.harutyunyan/Documents/AUA/group-2/BookFinder

# Start all services
docker-compose up --build

# Access:
# - Frontend: http://localhost:8501
# - Backend: http://localhost:8008
# - PgAdmin: http://localhost:5050
```

**✅ Frontend will connect to backend via: `http://backend:8000`**

### **Option 2: Local Development**

```bash
# Terminal 1: Backend
cd backend
# Start your backend on port 8000

# Terminal 2: Frontend  
cd frontend
export BACKEND_URL="http://localhost:8000"
streamlit run app_refactored.py
```

**✅ Frontend will connect to backend via: `http://localhost:8000`**

---

## 🐋 Docker Networking Explained

```
┌─────────────────────────────────────────────┐
│          Docker Network (app_default)       │
│                                             │
│  ┌──────────────┐      ┌──────────────┐   │
│  │  Frontend    │─────▶│   Backend    │   │
│  │  Container   │      │   Container  │   │
│  │              │      │              │   │
│  │ Connects to: │      │ Listens on:  │   │
│  │ backend:8000 │      │ port 8000    │   │
│  └──────────────┘      └──────────────┘   │
│        │                      │            │
│        │ Port mapping         │ Port       │
│        │ 8501:8501           │ mapping    │
│        │                      │ 8008:8000  │
└────────┼──────────────────────┼────────────┘
         │                      │
         ▼                      ▼
    localhost:8501         localhost:8008
    (Your browser)         (Your browser/curl)
```

**Key Points:**
- **Inside Docker**: Containers use service names (`backend:8000`)
- **Outside Docker**: We use localhost with mapped ports (`localhost:8008`)

---

## 🧪 Testing

### **Test Backend is Accessible**

```bash
# From your host machine
curl http://localhost:8008/

# From inside frontend container
docker exec -it streamlit_frontend curl http://backend:8000/
```

### **Test Frontend Connection**

1. Open http://localhost:8501
2. Try searching for a book
3. Should see results (no "Cannot connect" error)

---

## 🔍 Troubleshooting

### **Still getting "Cannot connect to backend"?**

1. **Check backend is running:**
   ```bash
   docker-compose ps
   # Should show backend as "Up"
   ```

2. **Check backend logs:**
   ```bash
   docker-compose logs backend
   ```

3. **Restart containers:**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

4. **Test backend directly:**
   ```bash
   curl http://localhost:8008/api/books/search?search_query=test
   ```

5. **Check environment variable is set:**
   ```bash
   docker exec streamlit_frontend env | grep BACKEND_URL
   # Should show: BACKEND_URL=http://backend:8000
   ```

---

## 📝 Summary of Changes

### **Changed Files:**

1. **`docker-compose.yml`**
   ```yaml
   # BEFORE:
   BACKEND_URL: "http://localhost:8000"
   
   # AFTER:
   BACKEND_URL: "http://backend:8000"
   ```

2. **`config/settings.py`**
   ```python
   # BEFORE:
   BACKEND_URL = "http://localhost:8000"
   
   # AFTER:
   BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
   ```

---

## ✅ Now It Works!

- ✅ Frontend in Docker connects to backend via service name
- ✅ Local development still works with localhost
- ✅ Environment-based configuration
- ✅ Flexible for different deployment scenarios

---

**You're all set! 🎉 Run `docker-compose up --build` and search should work!**
