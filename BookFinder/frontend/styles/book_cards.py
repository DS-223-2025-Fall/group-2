"""
Book card styles: card layout, cover, title, author, rating, buttons.
"""

def get_book_card_styles():
    """Returns CSS for book card components."""
    return """
    /* Style cards that have clickable buttons */
    /* Find the container (stVerticalBlock) that contains a card button */
    [data-testid="stVerticalBlock"]:has([class*="st-key-card_btn_"]) {
        position: relative !important;
        margin-bottom: 1.5rem;
    }
    
    /* Style the horizontal block (card content) inside containers with buttons */
    [data-testid="stVerticalBlock"]:has([class*="st-key-card_btn_"]) > [data-testid="stHorizontalBlock"] {
        background: var(--book-card-bg);
        border-radius: 22px;
        padding: 2rem 2.4rem;
        box-shadow: 0 16px 40px rgba(0,0,0,0.08);
        border: 1px solid var(--book-card-border);
        transition: all 0.3s ease;
        cursor: pointer;
        min-height: 220px;
    }
    
    [data-testid="stVerticalBlock"]:has([class*="st-key-card_btn_"]) > [data-testid="stHorizontalBlock"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 48px rgba(0,0,0,0.12);
        border-color: var(--logo-border);
    }
    
    /* Remove padding from columns inside the card */
    [data-testid="stVerticalBlock"]:has([class*="st-key-card_btn_"]) .stColumn {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Image column - fixed but larger width, centered image */
    [data-testid="stVerticalBlock"]:has([class*="st-key-card_btn_"]) > [data-testid="stHorizontalBlock"] > .stColumn:first-child {
        flex: 0 0 140px !important;
        max-width: 140px !important;
        min-width: 140px !important;
        display: flex !important;
        justify-content: center !important;
    }
    
    /* Book cover image - bigger */
    [data-testid="stVerticalBlock"]:has([class*="st-key-card_btn_"]) .stImage img {
        width: 120px !important;
        height: 170px !important;
        border-radius: 16px;
        object-fit: cover;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Content column should flex */
    [data-testid="stVerticalBlock"]:has([class*="st-key-card_btn_"]) > [data-testid="stHorizontalBlock"] > .stColumn:last-child {
        flex: 1 !important;
        min-width: 0 !important;
        padding-left: 1rem !important;
        position: relative !important;
    }
    
    /* Ensure text content wraps properly */
    [data-testid="stVerticalBlock"]:has([class*="st-key-card_btn_"]) .book-card-content {
        width: 100%;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Position the button to cover the parent vertical block (entire card) */
    .stElementContainer[class*="st-key-card_btn_"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 10 !important;
        margin: 0 !important;
        padding: 0 !important;
        pointer-events: auto !important;
    }
    
    .stElementContainer[class*="st-key-card_btn_"] .stButton {
        width: 100% !important;
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        pointer-events: auto !important;
    }
    
    .stElementContainer[class*="st-key-card_btn_"] button {
        width: 100% !important;
        height: 100% !important;
        opacity: 0.01 !important;
        cursor: pointer !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        pointer-events: auto !important;
        background: transparent !important;
        border-radius: 22px !important;
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

    """

