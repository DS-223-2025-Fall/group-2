# 🚨 CRITICAL: Docker Deployment Checklist

## ⚠️ Issues Found & Fixes Needed

Before your friend can test with Docker, you MUST make these changes:

---

## 🔴 ISSUE #1: Dockerfile Running Wrong File

### **Problem:**
`frontend/Dockerfile` is still running `app.py` instead of `app_refactored.py`

### **Current State:**
```dockerfile
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **Fix Required:**
```dockerfile
CMD ["streamlit", "run", "app_refactored.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **Why It Matters:**
- `app.py` = old monolithic code (no API integration)
- `app_refactored.py` = new code with API integration
- Docker will run the wrong file!

---

## 🔴 ISSUE #2: Wrong Backend URL in docker-compose.yml

### **Problem:**
Frontend trying to connect to `http://localhost:8000` instead of `http://backend:8000`

### **Current State:**
```yaml
environment:
  BACKEND_URL: "http://localhost:8000"  # ❌ WRONG
```

### **Fix Required:**
```yaml
environment:
  BACKEND_URL: "http://backend:8000"  # ✅ CORRECT
```

### **Why It Matters:**
- In Docker, containers can't use `localhost` to talk to each other
- Must use service name (`backend`) as hostname
- Without this, frontend will show "Cannot connect to backend"

---

## ✅ Quick Fix Commands

Run these commands to fix both issues:

### **Fix #1: Update Dockerfile**
```bash
cd /Users/ani.a.harutyunyan/Documents/AUA/group-2/BookFinder/frontend

# Edit Dockerfile, change line 9:
# FROM: CMD ["streamlit", "run", "app.py", ...]
# TO:   CMD ["streamlit", "run", "app_refactored.py", ...]
```

### **Fix #2: Update docker-compose.yml**
```bash
cd /Users/ani.a.harutyunyan/Documents/AUA/group-2/BookFinder

# Edit docker-compose.yml, change line 12:
# FROM: BACKEND_URL: "http://localhost:8000"
# TO:   BACKEND_URL: "http://backend:8000"
```

---

## 📋 Complete Fixed Files

### **frontend/Dockerfile** (Should Be):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_refactored.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **docker-compose.yml frontend section** (Should Be):
```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  container_name: streamlit_frontend
  ports:
    - "8501:8501"
  depends_on:
    - backend
  environment:
    BACKEND_URL: "http://backend:8000"  # ✅ Uses service name
    PYTHONWARNINGS: "ignore"
  restart: always
```

---

## 🧪 Testing After Fixes

### **Step 1: Build and Start**
```bash
cd /Users/ani.a.harutyunyan/Documents/AUA/group-2/BookFinder

# Stop existing containers
docker-compose down

# Rebuild and start
docker-compose up --build
```

### **Step 2: Verify Backend URL**
```bash
# Check environment variable is set correctly
docker exec streamlit_frontend env | grep BACKEND_URL
# Should show: BACKEND_URL=http://backend:8000
```

### **Step 3: Test Connection**
1. Open http://localhost:8501
2. Search for "anna" or any book
3. Should see: "🔍 Searching for books..." spinner
4. Should get results (not "Cannot connect" error)

### **Step 4: Test Backend Directly**
```bash
# From host machine
curl "http://localhost:8008/api/books/search?search_query=test"

# Should return JSON with books
```

---

## 📦 What Files Need to Be Committed

Before pushing to GitHub, make sure these files are updated:

```
✅ frontend/Dockerfile                    (Change app.py → app_refactored.py)
✅ docker-compose.yml                     (Change localhost → backend)
✅ frontend/config/settings.py            (Already done ✅)
✅ frontend/utils/api_client.py           (Already done ✅)
✅ frontend/utils/transformers.py         (Already done ✅)
✅ frontend/utils/search.py               (Already done ✅)
✅ frontend/components/*                  (Already done ✅)
✅ frontend/app_refactored.py             (Already done ✅)
```

---

## 🎯 Expected Behavior After Fixes

### **When Your Friend Runs:**
```bash
git clone <your-repo>
cd BookFinder
docker-compose up --build
```

### **What Should Happen:**
1. ✅ All containers start successfully
2. ✅ Frontend accessible at http://localhost:8501
3. ✅ Backend accessible at http://localhost:8008
4. ✅ Search works and returns results from backend
5. ✅ No "Cannot connect to backend" errors
6. ✅ Book cards display properly
7. ✅ View button navigates to detail page

---

## 🐛 Common Issues & Solutions

### **Issue: "Module not found" errors**
**Cause**: Missing __init__.py files  
**Solution**: All folders should have __init__.py (already created ✅)

### **Issue: "Cannot import from utils"**
**Cause**: Python path issues  
**Solution**: Already handled with relative imports ✅

### **Issue: Backend not starting**
**Cause**: Missing .env file or database issues  
**Solution**: Check backend logs with `docker-compose logs backend`

---

## ✨ Summary

### **MUST DO before pushing:**
1. ✅ Fix `frontend/Dockerfile` → change to `app_refactored.py`
2. ✅ Fix `docker-compose.yml` → change to `http://backend:8000`

### **Then:**
```bash
# Commit changes
git add .
git commit -m "Fix Docker configuration for API integration"
git push origin front

# Tell your friend to:
git pull origin front
docker-compose up --build
```

---

## 🎉 After These Fixes

Your friend will be able to:
- ✅ Clone the repo
- ✅ Run `docker-compose up --build`
- ✅ Access frontend at localhost:8501
- ✅ Search for books
- ✅ See results from backend API
- ✅ View book details
- ✅ Everything works perfectly!

**Ready to push after making these 2 fixes! 🚀**
