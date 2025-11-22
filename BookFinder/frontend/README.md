# FindMyRead - Refactored Structure

## Project Structure

```
frontend/
│
├── app.py                      # Original monolithic file (kept for reference)
├── app_refactored.py          # New clean entry point
│
├── components/                 # UI Components
│   ├── __init__.py
│   ├── home.py                # Home page view
│   ├── results.py             # Search results view
│   ├── detail.py              # Book detail view
│   └── book_card.py           # Reusable book card component
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── session.py             # Session state management & navigation
│   └── search.py              # Search and data retrieval functions
│
├── data/                       # Data layer
│   ├── __init__.py
│   └── books.py               # Mock book data (replace with API calls later)
│
├── styles/                     # Styling
│   ├── __init__.py
│   └── main_styles.py         # All CSS styles
│
└── config/                     # Configuration
    ├── __init__.py
    └── settings.py            # App configuration settings
```

## Key Improvements

### 1. **Separation of Concerns**
- **Components**: Each view (home, results, detail) is in its own file
- **Utils**: Business logic separated from UI
- **Data**: Data layer isolated for easy backend integration
- **Styles**: All CSS in one place, easy to maintain

### 2. **Maintainability**
- Each file has a single responsibility
- Easy to find and modify specific functionality
- Clear module boundaries

### 3. **Testability**
- Functions are isolated and can be tested independently
- Mock data is separated from business logic

### 4. **Scalability**
- Easy to add new views/components
- Simple to integrate with backend API (just replace data/books.py)
- Clear structure for team collaboration

## Running the Application

### Option 1: Run the refactored version (recommended)
```bash
streamlit run app_refactored.py
```

### Option 2: Run the original version
```bash
streamlit run app.py
```

## Module Descriptions

### `app_refactored.py`
Main entry point. Handles:
- Page configuration
- Applying styles
- Session state initialization
- Routing between views

### `components/`
- **home.py**: Home page with hero section and search bar
- **results.py**: Search results page with book listings
- **detail.py**: Detailed book information page
- **book_card.py**: Reusable component for displaying book cards

### `utils/`
- **session.py**: Manages session state and navigation functions
- **search.py**: Search logic and book retrieval functions

### `data/`
- **books.py**: Mock data for books and bookstores
(In production: Replace with API client/service layer)

### `styles/`
- **main_styles.py**: All CSS styling in one function

### `config/`
- **settings.py**: Application configuration constants


## Running the Frontend
### 1. Run Locally (without Docker)

Make sure you have Python 3.10+ installed.
```
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### 2. Running with Docker

#### Build the Docker image

From the root of the project:
``` bash
docker build -t frontend-service ./frontend
```
Run the container
``` bash
docker run --rm -p 8501:8501 frontend-service
```

## Dockerfile Summary

The Dockerfile:

- Uses `python:3.11-slim`
- Installs all dependencies from `requirements.txt`
- Copies the Streamlit app into `/app`
- Runs the app on port `8501`



## Next Steps for Production

1. **Backend Integration**
   - Replace `data/books.py` with API client
   - Add error handling for API calls
   - Implement caching

2. **Authentication**
   - Add user login/signup components
   - Session management for authenticated users

3. **Testing**
   - Add unit tests for utility functions
   - Integration tests for components

4. **Performance**
   - Implement lazy loading for book lists
   - Add pagination for search results

5. **Features**
   - Add filters (genre, price, rating)
   - Implement favorites/wishlist
   - Add book reviews section
