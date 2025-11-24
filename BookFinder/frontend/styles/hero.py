"""
Hero section styles: title, subtitle, search form.
"""

def get_hero_styles():
    """Returns CSS for hero section components."""
    return """
    /* Hero view - centered */
    .hero-wrapper {
        max-width: 1200px;
        margin: 0 auto 2rem auto;
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

    /* --- FIX SEARCH BAR CONTAINER SPACING --- */
    .search-container {
        width: 100%;
        max-width: 600px;
        margin: 0 auto !important;
        display: flex;
        flex-direction: column;
        gap: 0.75rem; /* spacing between label, input, and button */
        align-items: center; /* center-align elements inside */
    }

    /* --- MAKE SEARCH INPUT CENTER ALIGNED --- */
    .search-container .stTextInput > div > div {
        width: 100% !important;
    }

    /* --- CENTER THE SEARCH BUTTON --- */
    .search-container .stButton > button {
        margin: 0 auto !important;
        display: block !important;
    }

    /* --- OPTIONAL: ADD MORE VERTICAL SPACING ABOVE/BELOW SEARCH --- */
    .search-section {
        margin-top: 2rem;
        margin-bottom: 2rem;
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
    """

