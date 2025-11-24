"""
Sidebar styles: sidebar background, content, buttons.
"""

def get_sidebar_styles():
    """Returns CSS for sidebar components."""
    return """
    /* NUCLEAR option - completely eliminate sidebar from layout */
    .stSidebar,
    section.stSidebar,
    section[data-testid="stSidebar"],
    [aria-expanded="false"][data-testid="stSidebar"],
    .st-emotion-cache-mn9soh {
        display: none !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
        flex-shrink: 0 !important;
        position: absolute !important;
        left: -9999px !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    
    /* Hide sidebar buttons everywhere */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stExpandSidebarButton"],
    button[data-testid="stBaseButton-headerNoPadding"],
    .st-emotion-cache-13veyas,
    .st-emotion-cache-8ezv7j {
        display: none !important;
        visibility: hidden !important;
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
    """

