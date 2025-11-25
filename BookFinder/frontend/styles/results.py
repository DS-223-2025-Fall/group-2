"""
Results view styles: search results header, searchbar.
"""

def get_results_styles():
    """Returns CSS for results view components."""
    return """
    /* Results view - centered */
    .results-header {
        max-width: 1200px;
        margin: 1.4rem auto 1.8rem auto;
        padding: 0 2rem;
        text-align: center;
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
        padding: 0;
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
        border: 1px solid var(--logo-border) !important;
        padding: 0.45rem 1.5rem;
        font-weight: 600;
        color: var(--search-btn-text) !important;
    }
    """

