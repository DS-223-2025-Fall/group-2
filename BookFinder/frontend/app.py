import streamlit as st
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="FindMyRead", page_icon="�", layout="wide")

# ---------------- STYLES ----------------
DARK_VARS = """
:root {
--body-bg: #1a0f0a;
--container-bg: #0d0805;
--logo-border: #8b6a3b;
--moon-color: #d4b08a;
--hero-title: #f5e6d3;
--hero-subtitle: #c4a67d;
--search-bg: #2a1a12;
--search-shadow: 0 18px 40px rgba(0,0,0,0.3);
--search-icon: #b49a7a;
--search-btn-bg: #5f4b32;
--bookish-color: #a08f7b;
--strip-label: #b49a7a;
--strip-item-bg: #2a1a12;
--strip-item-color: #d4b08a;
--strip-icon-border: #8b6a3b;
--results-search-bg: #2a1a12;
--results-shadow: 0 10px 24px rgba(0,0,0,0.3);
--results-back: #b49a7a;
--results-icon: #b49a7a;
--results-btn-bg: #5f4b32;
--book-card-bg: #2a1a12;
--book-card-border: #5f4b32;
--book-cover-bg: linear-gradient(135deg, #8b6a3b, #5f4b32);
--book-title: #f5e6d3;
--book-author: #c4a67d;
--book-desc: #b49a7a;
--book-rating: #c4a67d;
--book-bottom-border: #5f4b32;
--book-store-color: #d4b08a;
--book-store-icon-border: #8b6a3b;
--book-store-name: #b49a7a;
--book-price: #f5e6d3;
--book-btn-bg: #5f4b32;
--book-btn-color: #f5e6d3;
}
"""

# ---------------- MOCK DATA (SIMULATION) ----------------
BOOKS = [
    {
        "id": 1,
        "title": "Anna Karenina",
        "author": "Leo Tolstoy",
        "description": "A tragic love story set in 19th century Russia.",
        "long_description": "Anna Karenina is a profound exploration of love, marriage, and societal expectations in 19th-century Russia. Tolstoy weaves multiple narratives that examine the moral complexities of human relationships, social mores, and the struggle between personal fulfillment and duty. The novel's sweeping scope and unforgettable characters make it a timeless classic.",
        "rating": 4.9,
        "store": {"name": "Bookinist", "price": 9500, "currency": "AMD"},
    },
    {
        "id": 2,
        "title": "The Name of the Rose",
        "author": "Umberto Eco",
        "description": "A medieval mystery set in an Italian monastery.",
        "long_description": "The Name of the Rose is a historical mystery set in 14th-century Italy, following Brother William of Baskerville as he investigates a series of murders at a Benedictine abbey. Eco overlays a richly researched medieval setting with philosophical debates, semiotics, and intricate plotting. This edition explores the tension between reason and faith through a dense, atmospheric narrative.",
        "rating": 4.5,
        "store": {"name": "Zangak", "price": 8500, "currency": "AMD"},
    },
    {
        "id": 3,
        "title": "The Name of the Rose (Epigraph Edition)",
        "author": "Umberto Eco",
        "description": "A medieval mystery set in an Italian monastery.",
        "long_description": "This special epigraph edition includes additional annotations and insights into Eco's layering of historical detail, literary allusion, and medieval scholarship. The story remains a tightly crafted mystery with philosophical undertones, enriched here by extra content and scholarly notes.",
        "rating": 4.5,
        "store": {"name": "Epigraph", "price": 9200, "currency": "AMD"},
    },
]

def simple_search(query: str):
    """Return (exact_matches, suggestions) from mock data."""
    q = query.lower().strip()
    if not q:
        return [], []
    exact = [b for b in BOOKS if q in b["title"].lower() or q in b["author"].lower()]
    if exact:
        suggestions = [b for b in BOOKS if b not in exact]
    else:
        suggestions = random.sample(BOOKS, min(3, len(BOOKS)))
    return exact, suggestions

def render_book_card(book: dict, book_id: int = None):
    """Render one book card as in your screenshot."""
    full_stars = int(round(book["rating"]))
    stars = "★" * full_stars + "☆" * (5 - full_stars)
    store = book["store"]
    html = f"""
    <div class="book-card">
      <div class="book-card-inner">
        <div class="book-cover"></div>
        <div class="book-main">
          <div class="book-title">{book['title']}</div>
          <div class="book-author">by {book['author']}</div>
          <div class="book-desc">{book['description']}</div>
          <div class="book-rating-row">
            <span class="book-stars">{stars}</span>
            <span class="book-rating-value">{book['rating']}</span>
          </div>
                    <div class="book-bottom-row">
            <div class="book-store-pill">
              <span class="book-store-icon"></span>
              <span>
                <span class="book-store-name">{store['name']}</span>
                <span class="book-price">{store['price']} {store['currency']}</span>
              </span>
            </div>
                        <!-- View button replaced by Streamlit widget below -->
          </div>
        </div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    # Render a real Streamlit button rather than relying on the markup-only view element
    if book_id is not None:
        # Align the button to the right by using nested columns
        c1, c2, c3 = st.columns([6, 1, 1])
        with c2:
            st.button("View", key=f"view_{book_id}", on_click=go_to_detail, args=(book_id,))

# ---------------- STATE ----------------
if "view" not in st.session_state:
    st.session_state["view"] = "home"
if "last_query" not in st.session_state:
    st.session_state["last_query"] = ""
if "exact" not in st.session_state:
    st.session_state["exact"] = []
if "suggestions" not in st.session_state:
    st.session_state["suggestions"] = []
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"
if "selected_book_id" not in st.session_state:
    st.session_state["selected_book_id"] = None

# Sync from query params (for browser back/forward)
query_params = st.query_params
if "view" in query_params:
    param_view = query_params["view"]
    if param_view in ["home", "results", "detail"]:
        st.session_state["view"] = param_view
        if param_view == "detail" and "book_id" in query_params:
            try:
                st.session_state["selected_book_id"] = int(query_params["book_id"])
            except ValueError:
                pass

CSS = "<style>" + """
:root {
--body-bg: #f5efe6;
--container-bg: #faf5ee;
--logo-border: #5f4b32;
--moon-color: #b19a7f;
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
""" + (DARK_VARS if st.session_state["theme"] == "dark" else "") + """
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
.app-moon {
    color: var(--moon-color);
    font-size: 1.2rem;
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

/* Theme toggle button */
.stButton > button {
    background: none !important;
    border: none !important;
    color: var(--moon-color) !important;
    font-size: 1.2rem !important;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ---------------- TOP BAR ----------------
col1, col2 = st.columns([10, 1])
with col1:
    st.markdown('<div class="app-logo"><div class="logo-icon">F</div><span>FindMyRead</span></div>', unsafe_allow_html=True)
with col2:
    def toggle_theme():
        st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"

    st.button("Dark" if st.session_state["theme"] == "light" else "Light", key="theme_toggle", on_click=toggle_theme)

def go_home():
    st.session_state["view"] = "home"
    st.session_state["last_query"] = ""
    st.session_state["exact"] = []
    st.session_state["suggestions"] = []
    st.session_state["selected_book_id"] = None
    st.query_params.clear()

def go_to_detail(book_id: int):
    st.session_state["view"] = "detail"
    st.session_state["selected_book_id"] = book_id
    st.query_params.update({"view": "detail", "book_id": str(book_id)})

def go_back_to_results():
    st.session_state["view"] = "results"
    st.query_params.update({"view": "results"})


def get_book_by_id(book_id: int):
    for b in BOOKS:
        if b.get("id") == book_id:
            return b
    return None


def render_book_detail(book: dict):
    # Fancy header with back button
    st.markdown("""
        <style>
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
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Results", key="detail_back"):
        go_back_to_results()
    
    # Header with title and author
    st.markdown(f"""
        <div class="detail-header">
            <div class="detail-title">{book['title']}</div>
            <div class="detail-author">by {book['author']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content: cover and metadata at left, long description at right
    st.markdown('<div class="detail-content">', unsafe_allow_html=True)
    left, right = st.columns([2, 5])
    
    with left:
        # Book cover
        st.markdown('<div class="detail-cover"></div>', unsafe_allow_html=True)
        
        # Rating with stars
        full_stars = int(round(book["rating"]))
        stars = "★" * full_stars + "☆" * (5 - full_stars)
        st.markdown(f"""
            <div class="detail-meta">
                <span class="detail-stars">{stars}</span>
                <span>{book['rating']} / 5</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Store info
        st.markdown(f"""
            <div class="detail-meta" style="margin-top: 1.5rem;">
                <div class="detail-meta-label">Available at:</div>
                <div style="font-size: 1.125rem; margin-top: 0.5rem;">{book['store']['name']}</div>
                <div style="font-size: 1.25rem; font-weight: 600; color: var(--book-price, #2c1810); margin-top: 0.25rem;">
                    {book['store']['price']} {book['store']['currency']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Buy button
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("Buy from Store", key=f"buy_{book.get('id')}", use_container_width=True):
            st.info(f"This would redirect to {book['store']['name']} in a real app.")
    
    with right:
        st.markdown(f"""
            <div class="detail-description">
                {book.get('long_description', book['description'])}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main navigation
if st.session_state["view"] == "home":
    # Hero
    st.markdown(
        """
        <div class="hero-wrapper">
            <div class="hero-title">Discover Your Next<br/>Literary Journey</div>
            <div class="hero-subtitle">
                Find your next read — or the closest one.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hero search
    center = st.columns([1, 2, 1])[1]
    with center:
        st.markdown('<div class="hero-search-wrapper">', unsafe_allow_html=True)
        with st.form("hero_search"):
            c1, c2 = st.columns([7, 2])
            with c1:
                st.markdown('<div class="hero-search-box">', unsafe_allow_html=True)
                st.markdown('<span class="hero-search-icon"></span>', unsafe_allow_html=True)
                query = st.text_input(
                    label="",
                    placeholder="Search for any book…",
                    label_visibility="collapsed",
                    key="hero_query",
                )
                st.markdown("</div>", unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="hero-search-button">', unsafe_allow_html=True)
                submit = st.form_submit_button("Search")
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="bookish-wrapper">Feeling Bookish?</div>', unsafe_allow_html=True)

    if submit and query:
        exact, suggestions = simple_search(query)
        st.session_state["view"] = "results"
        st.session_state["last_query"] = query
        st.session_state["exact"] = exact
        st.session_state["suggestions"] = suggestions
        st.query_params.update({"view": "results", "q": query})

    # Bottom bookstore strip
    st.markdown(
        '<div class="store-strip-label">Searching across trusted bookstores</div>',
        unsafe_allow_html=True,
    )
    strip_stores = ["Zangak", "Epigraph", "Books.am", "Nor Graxanut", "Phoenix", "Bookinist"]
    items = "".join(
        f'<div class="store-strip-item"><span class="store-strip-icon"></span><span>{s}</span></div>'
        for s in strip_stores
    )
    st.markdown(f'<div class="store-strip-badges">{items}</div>', unsafe_allow_html=True)

# ---------------- RESULTS VIEW ----------------
elif st.session_state["view"] == "results":
    # ---------------- RESULTS VIEW ----------------
    # Search bar with back arrow (results page)
    with st.form("results_search"):
        st.markdown('<div class="results-searchbar"><div class="results-search-inner">', unsafe_allow_html=True)
        col_back, col_icon, col_input, col_btn = st.columns([0.5, 0.6, 6, 2])
        with col_back:
            back_clicked = st.form_submit_button("←")
        with col_icon:
            st.markdown('<div class="results-search-icon"></div>', unsafe_allow_html=True)
        with col_input:
            query2 = st.text_input(
                "",
                value=st.session_state["last_query"],
                label_visibility="collapsed",
                key="results_query",
            )
        with col_btn:
            search_again = st.form_submit_button("Search")
        st.markdown("</div></div>", unsafe_allow_html=True)

    if back_clicked:
        go_home()

    if search_again and query2:
        exact, suggestions = simple_search(query2)
        st.session_state["last_query"] = query2
        st.session_state["exact"] = exact
        st.session_state["suggestions"] = suggestions
        st.query_params.update({"view": "results", "q": query2})

    exact = st.session_state["exact"]
    suggestions = st.session_state["suggestions"]
    query = st.session_state["last_query"]

    # Header text
    st.markdown('<div class="results-header">', unsafe_allow_html=True)
    if exact:
        st.markdown('<div class="result-title">Found in Bookstores</div>', unsafe_allow_html=True)
        count_text = f"{len(exact)} result" + ("s" if len(exact) != 1 else "")
        st.markdown(
            f'<div class="result-subtitle">{count_text} for "{query}"</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="result-title">You Might Like These</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="result-subtitle">We couldn’t find an exact match for "{query}", but here are some similar books</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Cards
    if exact:
        # Center each exact match card (usually just one)
        for book in exact:
            cols = st.columns([1, 2, 1])
            with cols[1]:
                render_book_card(book, book.get("id"))
            st.write("")
    else:
        # Grid of recommended books
        st.markdown('<div class="recommend-grid">', unsafe_allow_html=True)
        for book in suggestions:
            st.markdown("<div>", unsafe_allow_html=True)
            render_book_card(book, book.get("id"))
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- DETAIL VIEW ----------------
elif st.session_state["view"] == "detail":
    selected_id = st.session_state.get("selected_book_id")
    b = get_book_by_id(selected_id)
    if b is None:
        st.warning("Book not found.")
        go_back_to_results()
    else:
        render_book_detail(b)
