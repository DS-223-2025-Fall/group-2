"""
Styles module for FindMyRead application.
Contains all CSS styling for the Streamlit app.
"""

def get_styles():
    """Returns the complete CSS styles for the application."""
    return """
    <style>
    :root {
    --body-bg: #f5efe6;
    --container-bg: #faf5ee;
    --logo-border: #5f4b32;
    --hero-title: #5b4730;
    --hero-subtitle: #7f6a4d;
    --search-bg: #ffffff;
    --search-shadow: 0 18px 40px rgba(0,0,0,0.08);
    --search-icon: #a08f7b;
    --search-btn-bg: #8b6a3b;
    --bookish-color: #7a6750;
    --strip-label: #8a7a63;
    --strip-item-bg: #f2ebe1;
    --strip-item-color: #5e4a32;
    --strip-icon-border: #a08f7b;
    --results-search-bg: #ffffff;
    --results-shadow: 0 10px 24px rgba(0,0,0,0.05);
    --results-back: #8a7a63;
    --results-icon: #a08f7b;
    --results-btn-bg: #8b6a3b;
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
    --book-btn-bg: #8b6a3b;
    --book-btn-color: #fffaf2;
    }
    
    body {
        background: var(--body-bg);
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        background: var(--container-bg);
    }
    [data-testid="stHeader"] {
        background: rgba(255,255,255,0.0);
    }

    /* Top logo bar */
    .app-topbar {
        padding: 0.6rem 1.4rem 0.4rem 1.4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .app-logo {
        font-weight: 700;
        font-size: 1.3rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        color: #5f4b32;
        font-family: Georgia, 'Times New Roman', serif;
    }
    .logo-icon {
        width: 26px;
        height: 26px;
        border-radius: 8px;
        border: 2px solid var(--logo-border);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
    }

    /* Make all text inputs look like your dark bar */
    div[data-testid="stTextInput"] input {
        background: #232429;
        color: #ffffff;
        border-radius: 999px;
        border: none;
        padding: 0.8rem 1.2rem;
    }

    /* Hero view */
    .hero-wrapper {
        margin-top: 3.2rem;
        text-align: center;
    }
    .hero-title {
        font-size: 3rem;
        line-height: 1.1;
        font-weight: 700;
        color: var(--hero-title);
    }
    .hero-subtitle {
        margin-top: 0.7rem;
        font-size: 1.05rem;
        color: var(--hero-subtitle);
    }

    /* Search on hero */
    .hero-search-wrapper {
        margin: 2.4rem auto 1.1rem auto;
        max-width: 640px;
    }
    .hero-search-box {
        background: var(--search-bg);
        border-radius: 999px;
        padding: 0.25rem 0.4rem;
        box-shadow: var(--search-shadow);
        display: flex;
        align-items: center;
    }
    .hero-search-icon {
        margin-left: 1.1rem;
        margin-right: 0.6rem;
        font-size: 1rem;
        color: var(--search-icon);
    }
    .hero-search-input > div > div > input {
        border-radius: 999px;
        border: none !important;
        box-shadow: none !important;
    }

    /* Optional: remove extra spacing */
    div[data-testid="stTextInput"] {
        margin-bottom: 0;
    }

    .hero-search-button > button {
        border-radius: 999px;
        background: var(--search-btn-bg) !important;
        border: none;
        padding: 0.6rem 1.8rem;
        font-weight: 600;
    }

    /* "Feeling bookish" */
    .bookish-wrapper {
        text-align: center;
        margin-top: 0.6rem;
        color: var(--bookish-color);
        font-size: 0.95rem;
    }

    /* Bottom bookstore strip */
    .store-strip-label {
        margin-top: 3rem;
        text-align: center;
        font-size: 0.95rem;
        color: var(--strip-label);
    }
    .store-strip-badges {
        margin-top: 0.6rem;
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 0.9rem;
    }
    .store-strip-item {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        background: var(--strip-item-bg);
        font-size: 0.9rem;
        color: var(--strip-item-color);
    }
    .store-strip-icon {
        width: 20px;
        height: 20px;
        border-radius: 6px;
        border: 1px solid var(--strip-icon-border);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
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
        border: none;
        padding: 0.45rem 1.5rem;
        font-weight: 600;
    }

    /* Book cards */
    .book-card {
        background: var(--book-card-bg);
        border-radius: 22px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 16px 40px rgba(0,0,0,0.08);
        border: 1px solid var(--book-card-border);
    }
    .book-card-inner {
        display: flex;
        gap: 1rem;
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

    .book-view-btn {
        padding: 0.45rem 1.2rem;
        border-radius: 999px;
        background: var(--book-btn-bg);
        color: var(--book-btn-color);
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* Grid for "You might like these" */
    .recommend-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 1.4rem;
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
    .detail-content {
        background: var(--book-card-bg, #f5f1e8);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid var(--book-card-border, #d4c5a9);
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
    </style>
    """
