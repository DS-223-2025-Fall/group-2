"""
Navigation styles: top navbar, logo, login button.
"""

def get_navigation_styles():
    """Returns CSS for navigation and header components."""
    return """
    /* Remove all padding from columns */
    [data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Target the navbar - first horizontal block after navbar-wrapper */
    .main .block-container > div:has(.navbar-wrapper) ~ [data-testid="stHorizontalBlock"]:first-of-type,
    .main .block-container > [data-testid="stHorizontalBlock"]:first-of-type {
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw !important;
        margin-right: -50vw !important;
        width: 100vw !important;
        max-width: 100vw !important;
        padding: 0.5rem 2rem !important;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* First column (logo) - shrink to fit content */
    .main .block-container > [data-testid="stHorizontalBlock"]:first-of-type > div:first-child {
        flex: 0 0 auto !important;
        min-width: auto !important;
    }
    
    /* Last column (login) - shrink to fit content and align right */
    .main .block-container > [data-testid="stHorizontalBlock"]:first-of-type > div:last-child {
        flex: 0 0 auto !important;
        min-width: auto !important;
        margin-left: auto !important;
    }
    
    /* Logo - align to the left */
    .app-logo {
        font-weight: 700;
        font-size: 1.4rem;
        display: flex;
        align-items: center;
        gap: 0;
        color: #5f4b32;
        font-family: 'Merriweather', Georgia, 'Times New Roman', serif;
    }
    
    .app-logo span {
        margin-left: 0.15rem; /* tiny manual spacing */
    }
    
    .logo-icon {
        width: 36px;
        height: 36px;
        min-width: 36px;
        min-height: 36px;
        aspect-ratio: 1 / 1;
        border-radius: 10px;
        border: 2.5px solid var(--logo-border);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        font-weight: 700;
        line-height: 1;
        background: linear-gradient(135deg, rgba(95,75,50,0.08), rgba(95,75,50,0.03));
        box-sizing: border-box;
        flex-shrink: 0;
    }

    /* Login button styling - align to the right */
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
        float: right !important;
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
    
    /* Third column (login) - align content to right */
    [data-testid="stHorizontalBlock"] > div:last-child [data-testid="column"] {
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    """

