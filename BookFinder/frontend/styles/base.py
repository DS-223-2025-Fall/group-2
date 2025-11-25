"""
Base styles: CSS variables, fonts, animations, and global resets.
"""

def get_base_styles():
    """Returns base CSS including variables, fonts, animations, and global styles."""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@700&display=swap');
    
    /* Hide Streamlit UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    
    /* CSS Variables */
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
    
    /* Global styles */
    body {
        background: #f5efe6;
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
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
    """

