"""
Layout styles: page structure, containers, spacing.
"""

def get_layout_styles():
    """Returns CSS for page layout and containers."""
    return """
    /* Page background and scrolling setup */
    html {
        background-color: #faf5ee !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        height: auto !important;
    }
    
    body {
        background-color: #faf5ee !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        height: auto !important;
    }
    
    .stApp {
        background-color: #faf5ee !important;
        margin: 0 !important;
        padding: 0 !important;
        min-height: 100vh !important;
        height: auto !important;
        overflow-y: visible !important;
    }

    /* Main container - NO padding whatsoever */
    .main, .stMain, section[data-testid="stMain"] {
        padding: 0 !important;
        padding-bottom: 3rem !important;
        margin: 0 !important;
        width: 100% !important;
        height: auto !important;
        min-height: 100vh !important;
        max-height: none !important;
        overflow: visible !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #faf5ee !important;
        padding: 0 !important;
        height: auto !important;
        min-height: 100vh !important;
        max-height: none !important;
        overflow: visible !important;
    }
    
    /* Ensure all parent containers can expand */
    .stAppViewContainer, .appview-container {
        height: auto !important;
        min-height: 100vh !important;
        max-height: none !important;
    }
    
    .main .block-container,
    .stMainBlockContainer,
    [data-testid="stMainBlockContainer"] {
        max-width: 1200px !important;
        padding: 0 !important;
        margin: 0 auto !important;
        width: 100% !important;
        height: auto !important;
        max-height: none !important;
    }
    
    /* Allow vertical blocks to expand */
    [data-testid="stVerticalBlock"] {
        height: auto !important;
        max-height: none !important;
    }
    
    /* Target Streamlit's emotion-cache classes */
    .st-emotion-cache-zy6yx3,
    .st-emotion-cache-4rsbii,
    .st-emotion-cache-1yiq2ps,
    .st-emotion-cache-6px8kg,
    .st-emotion-cache-1r4qj8v {
        padding: 0 !important;
        margin: 0 !important;
        height: auto !important;
        max-height: none !important;
        overflow: visible !important;
    }
    
    /* Force all emotion-cache containers to allow overflow */
    div[class*="st-emotion-cache"] {
        max-height: none !important;
    }
    
    /* Remove padding from key layout elements only */
    [data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Center text */
    .hero-title, .hero-subtitle, h1, h2, h3, p {
        text-align: center !important;
    }
    
    /* Make navbar wrapper break out to full width */
    .navbar-wrapper {
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw !important;
        margin-right: -50vw !important;
        width: 100vw !important;
        max-width: 100vw !important;
        padding: 0.5rem 2rem !important;
    }
    
    /* Style the navbar columns container */
    .navbar-wrapper + [data-testid="stHorizontalBlock"] {
        width: 100% !important;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    """

