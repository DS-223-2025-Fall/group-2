"""
Responsive styles: media queries for different screen sizes.
"""

def get_responsive_styles():
    """Returns CSS media queries for responsive design."""
    return """
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
    """

