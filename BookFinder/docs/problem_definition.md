# Problem Definition

## 1. Identify the Problem Area
The project is part of the **Product Development and Customer Experience** area of marketing. It focuses on solving the difficulties readers in **Yerevan** face when trying to find and buy books from local bookstores.  

Since local stores have separate websites, it is hard for people to:

- Check where a book is available

- Compare prices

- Find good options for reading or gifting  

This lack of centralized information reduces local bookstore sales and increases reliance on foreign online retailers.

---

## 2. Conduct Preliminary Research
Preliminary research reveals that:

- Many Yerevan bookstores, such as **Bookinist**, **Books.am**, and **Zangak**, have separate online platforms that are not integrated, making it difficult for customers to know where a specific book is available or at what price.
- Customers often spend considerable time comparing availability and prices across different stores or end up ordering from international websites, increasing waiting time and costs.
- Recommender systems and product-matching algorithms are widely used in e-commerce but are rarely applied to local offline bookstores.
- Studies show that personalized recommendation systems and price optimization significantly improve customer satisfaction and local business engagement.

**Opportunity:** Create a unified platform that enhances book discovery and supports local retail through intelligent search and recommendation.

---

## 3. Define a Specific Problem
**Problem Statement:**  
How can we design a **data-driven recommendation platform** that allows users to find the availability, price, and location of a desired book in Yerevan, and if unavailable, suggests the most similar locally available books based on plot, genre, and description?

---

## 4. Propose a Solution with Methodology

### A. Data Collection
Data will be collected by scraping websites of major bookstores in Yerevan (e.g., Bookinist, Books, Zangak). The scraped data will include:

- Book details: title, author, genre, plot/description, publication year, ISBN  
- Price and availability  
- Store information: name and address  

Global book databases such as **Google Books API** or **Open Library API** will also be used to retrieve plot summaries and metadata for similarity-based recommendations.

### B. Analytical Techniques
The analytical component includes two major stages:

1. **Exact Match Retrieval**
   - Fuzzy-matching techniques will identify the most accurate match between the user’s query and the books in the Yerevan database.
   - When multiple stores have the same book, the optimal option will be chosen based on **price ranking**.

2. **Similarity-Based Recommendation**
   - If the book is not available, or even if it is, a list of similar books will be generated using **classic ML and DL models**.

### C. Implementation Plan
1. **Database Construction:** Build a comprehensive dataset of books in Yerevan through regular web scraping.  
2. **Search Engine Development:** Implement a query processing system that matches user input with the most relevant book titles.  
3. **Recommendation Module:** Integrate an ML-based recommendation engine to suggest similar books.  
4. **Deployment and Evaluation:** Launch a functional prototype website, allowing user testing.  

---

## 5. Expected Outcomes

- **For users:** Reduced time spent searching for books and improved satisfaction through personalized, local availability suggestions.  
- **For bookstores:** Increased sales and visibility by appearing in user search results and recommendations.  
- **For the market:** Strengthened customer engagement with local book retailers, reducing reliance on foreign e-commerce sites.  
- **For data insights:** Opportunity to analyze customer search trends and preferences in the Yerevan book market.  

---

## 6. Evaluation Metrics
Key Performance Indicators (KPIs) to measure success:

1. User satisfaction score  
2. Local store engagement increase  
3. Click-Through Rate  
4. Search Accuracy  
5. Response Time  

---

## 7. Summary
This project uses **marketing analytics and recommendation techniques** to solve a real-world consumer challenge: the difficulty of discovering and purchasing books locally in Yerevan.  

By combining **data scraping** and **ML-based similarity modeling**, the proposed solution creates tangible value for both customers and local businesses. It demonstrates how well-implemented recommendation systems can improve local retail engagement.
