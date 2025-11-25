"""
Detail view styles: book detail page layout.
"""

def get_detail_styles():
    """Returns CSS for book detail page."""
    return """
    /* Detail view styles - centered */
    .detail-header {
        max-width: 1200px;
        margin: 0 auto 2rem auto;
        padding: 2rem;
        background: linear-gradient(135deg, var(--book-card-bg, #f5f1e8) 0%, var(--container-bg, #faf8f3) 100%);
        border-radius: 12px;
        border: 1px solid var(--book-card-border, #d4c5a9);
        text-align: center;
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
    """

