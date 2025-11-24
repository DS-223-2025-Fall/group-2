"""
Styles module for FindMyRead application.
Contains all CSS styling for the Streamlit app.
"""

def get_styles():
    """Returns the complete CSS styles for the application."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@700&display=swap');
    
    :root {
    --body-bg: #f5efe6;
    --container-bg: #faf5ee;
    --logo-border: #5f4b32;
    --hero-title: #4a3720;
    --hero-subtitle: #7f6a4d;
    --search-bg: #ede6da;
    --search-text: #4a3720;
    --search-container-bg: #f2ebe1;
    --search-shadow: 0 8px 32px rgba(0,0,0,0.08);
    --search-icon: #7f6a4d;
    --search-btn-bg: #f3eadc;
    --search-btn-hover: #e6d8c5;
    --search-btn-text: #4a3720;
    --bookish-color: #7a6750;
    --strip-label: #8a7a63;
    --strip-container-bg: rgba(242,235,225,0.5);
    --strip-item-bg: #ede6da;
    --strip-item-hover: #e2d8ca;
    --strip-item-active: #c9b89d;
    --strip-item-color: #5e4a32;
    --strip-icon-border: #a08f7b;
    --results-search-bg: #ffffff;
    --results-shadow: 0 10px 24px rgba(0,0,0,0.05);
    --results-back: #8a7a63;
    --results-icon: #a08f7b;
    --results-btn-bg: #f3eadc;
    --book-card-bg: #fffdf8;
    --book-card-border: #efe1ce;
    --book-cover-bg: linear-gradient(135deg, #b49a7a, #6e5840);
    --book-title: #3f301e;
    --book-author: #7b6a53;
    --book-desc: #6a5a45;
    --book-rating: #7b6a53;
    --book-bottom-border: #eee0cf;
    --book-store-color: #6b5942;
    --book-store-icon-border: #b29f84;
    --book-store-name: #8b785e;
    --book-price: #3f301e;
    --book-btn-bg: #f3eadc;
    --book-btn-color: #4a3720;
    --navbar-bg: transparent;
    --navbar-shadow: none;
    --login-btn-bg: #f3eadc;
    --login-btn-hover: #e6d8c5;
    --login-btn-text: #4a3720;
    }
    
    /* Keyframe animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    body {
        background: #f5efe6;
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        background: #faf5ee;
        max-width: 1400px;
        margin: 0 auto;
    }
    [data-testid="stHeader"] {
        background: rgba(255,255,255,0.0);
    }

    /* Global text color - force all text to be dark */
    body, p, span, div, h1, h2, h3, h4, h5, h6, li, label, [data-testid="stMarkdownContainer"] {
        color: #4a3720 !important;
    }
    
    [data-testid="stMarkdownContainer"] p, 
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] div {
        color: #4a3720 !important;
    }

    /* Global button styling - all buttons beige with dark text */
    button, .stButton > button, button[kind="primary"], button[kind="secondary"] {
        background: var(--login-btn-bg) !important;
        color: var(--login-btn-text) !important;
        border: 1px solid var(--logo-border) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
    }
    
    button:hover, .stButton > button:hover, button[kind="primary"]:hover, button[kind="secondary"]:hover {
        background: var(--login-btn-hover) !important;
        color: var(--login-btn-text) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.08) !important;
    }
    
    button:active, .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    }

    /* Top navbar styling */
    .app-topbar {
        padding: 0.3rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: transparent;
        margin-bottom: 0.5rem;
    }
    
    .app-logo {
        font-weight: 700;
        font-size: 1.4rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #5f4b32;
        font-family: 'Merriweather', Georgia, 'Times New Roman', serif;
    }
    
    .logo-icon {
        width: 32px;
        height: 32px;
        border-radius: 10px;
        border: 2.5px solid var(--logo-border);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        font-weight: 700;
        background: linear-gradient(135deg, rgba(95,75,50,0.08), rgba(95,75,50,0.03));
    }

    /* Sidebar styling - beige background */
    [data-testid="stSidebar"] {
        background: #e8dcc8 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: #e8dcc8 !important;
    }
    
    /* Sidebar content styling */
    [data-testid="stSidebar"] h3 {
        color: #4a3720 !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #4a3720 !important;
    }
    
    /* Info box in sidebar - remove background and border */
    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background: transparent !important;
        border: none !important;
        color: #4a3720 !important;
        padding: 0.5rem 0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stAlert"] p {
        color: #4a3720 !important;
        margin: 0 !important;
    }
    
    /* Hide the info icon in sidebar but keep text visible */
    [data-testid="stSidebar"] [data-testid="stAlert"] svg {
        display: none !important;
    }
    
    /* Sidebar horizontal rule */
    [data-testid="stSidebar"] hr {
        border-color: #c9b89d !important;
        opacity: 0.5;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] button {
        background: var(--login-btn-bg) !important;
        color: var(--login-btn-text) !important;
        border: 1px solid var(--logo-border) !important;
    }

    /* Login button styling: light background, dark text, thin border */
    button[key="header_login"] {
        background: var(--login-btn-bg) !important;
        color: var(--login-btn-text) !important;
        border: 1px solid var(--logo-border) !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.4rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
        cursor: pointer !important;
    }
    
    button[key="header_login"]:hover {
        background: var(--login-btn-hover) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.08) !important;
    }
    
    button[key="header_login"]:active {
        transform: translateY(0);
        box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    }

    /* Make all text inputs light background */
    div[data-testid="stTextInput"] input {
        background: var(--search-bg) !important;
        color: var(--search-text) !important;
        border-radius: 8px !important;
        border: 1.5px solid #d0c4b0 !important;
        padding: 0.85rem 1.2rem !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
        outline: none !important;
        height: 52px !important;
        box-sizing: border-box !important;
    }
    
    /* Fix BaseWeb container styling */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 8px !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        box-shadow: 0 0 0 2px rgba(127,106,77,0.15) !important;
        outline: none !important;
        border: 1.5px solid #b5a797 !important;
    }
    
    div[data-testid="stTextInput"] input:focus-visible {
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(127,106,77,0.15) !important;
    }
    
    div[data-testid="stTextInput"] input::placeholder {
        color: rgba(127,106,77,0.6) !important;
    }

    /* Hero view */
    .hero-wrapper {
        margin-top: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        padding: 0 2rem;
    }
    
    .hero-title {
        font-size: 3.3rem;
        line-height: 1.15;
        font-weight: 700;
        color: var(--hero-title);
        font-family: 'Merriweather', Georgia, serif;
        letter-spacing: -0.02em;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        margin-top: 0.4rem;
        font-size: 1.2rem;
        color: var(--hero-subtitle);
        font-weight: 400;
        letter-spacing: 0.01em;
    }

    /* Hero search form - horizontal layout */
    div[data-testid="stForm"][aria-label="hero_search"] {
        margin: 1.5rem auto 1rem auto;
        max-width: 850px;
        padding: 0;
    }
    
    /* Make form columns align horizontally without gaps */
    div[data-testid="stForm"][aria-label="hero_search"] [data-testid="column"] {
        padding: 0 !important;
        gap: 0.5rem !important;
    }
    
    div[data-testid="stForm"][aria-label="hero_search"] [data-testid="stHorizontalBlock"] {
        gap: 0.5rem !important;
    }

    .search-helper-text {
        text-align: center;
        margin-top: 0.8rem;
        font-size: 0.9rem;
        color: var(--bookish-color);
        font-style: italic;
    }

    /* Search button styling: compact with border */
    button[type="submit"] {
        background: #ffffff !important;
        color: var(--search-btn-text) !important;
        border: 1.5px solid #d0c4b0 !important;
        border-radius: 8px !important;
        padding: 0.85rem 1.8rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        box-shadow: none !important;
        margin: 0 !important;
        white-space: nowrap !important;
        height: 52px !important;
    }
    
    button[type="submit"]:hover {
        background: #f8f6f3 !important;
        border-color: #b5a797 !important;
        transform: translateY(0);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    
    button[type="submit"]:active {
        transform: translateY(0);
        background: #f0ede8 !important;
        box-shadow: none !important;
    }

    /* Hide "Press Enter to submit form" helper text */
    [data-testid="stForm"] [data-testid="InputInstructions"] {
        display: none !important;
    }
    
    [data-testid="stForm"] div[class*="instructions"] {
        display: none !important;
    }

    /* Bottom bookstore strip */
    .store-strip-container {
        margin-top: 10rem;
    }
    
    .store-strip-label {
        text-align: center;
        font-size: 1rem;
        color: var(--strip-label);
        font-weight: 500;
        margin-bottom: 1.2rem;
    }
    
    .store-strip-badges {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 1rem;
        padding: 0 1rem 2rem 1rem;
    }
    
    .store-strip-item {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 1.2rem;
        border-radius: 999px;
        background: var(--strip-item-bg);
        font-size: 0.95rem;
        color: var(--strip-item-color);
        font-weight: 500;
        border: 1px solid rgba(95,75,50,0.35);
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .store-strip-item:hover {
        background: var(--strip-item-hover);
        border-color: rgba(95,75,50,0.6);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .store-strip-item:active,
    .store-strip-item.active {
        background: var(--strip-item-active);
        border-color: rgba(95,75,50,0.9);
        transform: translateY(0);
        font-weight: 600;
    }

    /* Optional: remove extra spacing */
    div[data-testid="stTextInput"] {
        margin-bottom: 0;
    }

    /* Results view */
    .results-header {
        margin-top: 1.4rem;
        margin-bottom: 1.8rem;
    }
    .result-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--hero-title);
    }
    .result-subtitle {
        font-size: 1rem;
        margin-top: 0.4rem;
        color: var(--hero-subtitle);
    }

    .results-searchbar {
        margin-top: 0.6rem;
        margin-bottom: 1.6rem;
        padding: 0 2rem;
    }
    .results-search-inner {
        background: var(--results-search-bg);
        border-radius: 999px;
        padding: 0.25rem 0.4rem;
        box-shadow: var(--results-shadow);
        display: flex;
        align-items: center;
    }
    .results-back {
        font-size: 1.2rem;
        margin-right: 0.6rem;
        color: var(--results-back);
    }
    .results-search-icon {
        margin-right: 0.6rem;
        font-size: 1rem;
        color: var(--results-icon);
    }
    .results-search-input > div > div > input {
        border-radius: 999px;
        border: none !important;
        box-shadow: none !important;
    }
    .results-search-button > button {
        border-radius: 999px;
        background: var(--results-btn-bg) !important;
        border: 1px solid var(--logo-border) !important;
        padding: 0.45rem 1.5rem;
        font-weight: 600;
        color: var(--search-btn-text) !important;
    }

    /* Book cards */
    .book-card-container {
        position: relative;
        margin-bottom: 1.5rem;
        width: 100%;
    }
    
    .book-card {
        background: var(--book-card-bg);
        border-radius: 22px;
        padding: 1.2rem 1.4rem 1.2rem 1.4rem;
        box-shadow: 0 16px 40px rgba(0,0,0,0.08);
        border: 1px solid var(--book-card-border);
        margin-bottom: 0 !important;
        width: 100%;
        box-sizing: border-box;
    }
    
    .book-card-inner {
        display: flex;
        gap: 1rem;
    }
    
    /* Style for book cover images */
    .book-card-inner img {
        width: 94px;
        height: 130px;
        border-radius: 16px;
        object-fit: cover;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Style columns to prevent extra spacing */
    .book-card-inner > div[data-testid="column"] {
        padding: 0 !important;
        gap: 0 !important;
    }
    
    .book-card-inner > div[data-testid="column"]:first-child {
        max-width: 94px !important;
        min-width: 94px !important;
    }
    
    .book-cover {
        width: 94px;
        height: 130px;
        border-radius: 16px;
        background: var(--book-cover-bg);
    }
    .book-main {
        flex: 1;
    }
    .book-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: var(--book-title);
    }
    .book-author {
        font-size: 0.95rem;
        color: var(--book-author);
        margin-top: 0.2rem;
    }
    .book-desc {
        font-size: 0.9rem;
        color: var(--book-desc);
        margin-top: 0.5rem;
    }
    .book-rating-row {
        margin-top: 0.5rem;
        font-size: 0.9rem;
        color: var(--book-rating);
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    .book-stars {
        letter-spacing: 0.08em;
    }
    .book-rating-value {
        margin-left: 0.1rem;
    }

    /* Bottom row inside card */
    .book-bottom-row {
        margin-top: 0.7rem;
        padding-top: 0.7rem;
        border-top: 1px solid var(--book-bottom-border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        min-height: 40px;
    }
    
    .book-view-btn-wrapper {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        flex-shrink: 0;
        margin-left: auto;
    }
    
    /* The actual "View" button inside the card */
    .book-view-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.45rem 1.2rem;
        border-radius: 999px;
        background: var(--book-btn-bg);
        color: var(--book-btn-color) !important;
        font-size: 0.9rem;
        font-weight: 600;
        border: 1px solid var(--logo-border);
        text-decoration: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        transition: all 0.2s ease;
        cursor: pointer;
        white-space: nowrap;
    }
    
    .book-view-btn:hover {
        background: var(--login-btn-hover);
        color: var(--book-btn-color) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    
    .book-store-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 0.9rem;
        color: var(--book-store-color);
    }
    .book-store-icon {
        width: 26px;
        height: 26px;
        border-radius: 9px;
        border: 1px solid var(--book-store-icon-border);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
    }
    .book-store-name {
        display: block;
        font-size: 0.8rem;
        color: var(--book-store-name);
    }
    .book-price {
        font-weight: 600;
        font-size: 1rem;
        color: var(--book-price);
    }

    /* Grid for "You might like these" */
    .recommend-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 1.4rem;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* For exact results - ensure consistent width */
    .exact-results-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Detail view styles */
    .detail-header {
        background: linear-gradient(135deg, var(--book-card-bg, #f5f1e8) 0%, var(--container-bg, #faf8f3) 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid var(--book-card-border, #d4c5a9);
    }
    .detail-title {
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--book-title, #2c1810);
        margin-bottom: 0.5rem;
    }
    .detail-author {
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 1.25rem;
        color: var(--book-author, #7b6a53);
        font-style: italic;
    }
    
    /* Style for detail page book images */
    div[data-testid="column"] img {
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        object-fit: cover;
        width: 100%;
    }
    
    .detail-cover {
        width: 220px;
        height: 320px;
        background: var(--book-cover-bg, linear-gradient(135deg, #8b6a3b, #5f4b32));
        border-radius: 8px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        margin-bottom: 1.5rem;
    }
    .detail-meta {
        font-size: 1rem;
        line-height: 1.8;
        color: var(--book-desc, #6b5d4f);
    }
    .detail-meta-label {
        font-weight: 600;
        color: var(--book-title, #2c1810);
    }
    .detail-description {
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 1.125rem;
        line-height: 1.8;
        color: var(--book-desc, #4a4035);
        text-align: justify;
        margin-bottom: 1.5rem;
    }
    .detail-stars {
        color: #d4af37;
        font-size: 1.25rem;
        margin-right: 0.5rem;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
            line-height: 1.2;
        }
        
        .hero-subtitle {
            font-size: 1rem;
        }
        
        .hero-wrapper {
            margin-top: 2rem;
            padding: 0 1rem;
        }
        
        div[data-testid="stForm"][aria-label="hero_search"] {
            padding: 1.2rem 1.4rem;
            margin-top: 1.6rem;
        }
        
        div[data-testid="stTextInput"] input {
            padding: 0.8rem 1.2rem !important;
            font-size: 0.95rem !important;
        }
        
        button[type="submit"] {
            padding: 0.8rem 1.5rem !important;
            font-size: 0.95rem !important;
        }
        
        .app-logo {
            font-size: 1.2rem;
        }
        
        .logo-icon {
            width: 28px;
            height: 28px;
        }
        
        .store-strip-badges {
            gap: 0.7rem;
        }
        
        .store-strip-item {
            padding: 0.5rem 1rem;
            font-size: 0.85rem;
        }
        
        .app-topbar {
            padding: 0.6rem 1rem;
            margin-bottom: 0.75rem;
        }
    }
    
    @media (max-width: 480px) {
        .hero-title {
            font-size: 2.1rem;
        }
        
        .hero-subtitle {
            font-size: 0.9rem;
        }
        
        .hero-wrapper {
            margin-top: 1.6rem;
        }
        
        .store-strip-container {
            margin-top: 15rem;
            padding: 0 1rem 1.2rem 1rem;
        }
        
        button[key="header_login"] {
            padding: 0.5rem 1rem !important;
            font-size: 0.85rem !important;
        }
    }
    </style>
    """
