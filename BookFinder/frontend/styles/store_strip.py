"""
Store strip styles: bottom bookstore badges.
"""

def get_store_strip_styles():
    """Returns CSS for bookstore strip at bottom of page."""
    return """
    /* Bottom bookstore strip - centered */
    .store-strip-container {
        max-width: 1200px;
        margin: 10rem auto 0 auto;
        padding: 0 2rem;
        text-align: center;
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
    """

