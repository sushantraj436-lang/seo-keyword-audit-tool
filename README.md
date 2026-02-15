# 🔍 SEO Keyword Audit Tool

A Python-based SEO audit prototype built to analyze on-page keyword usage from a given URL.  
This tool extracts webpage content, processes text data, and generates structured JSON output highlighting frequently used service-related keywords.

---

## 🎯 Project Objective

The purpose of this project is to understand how SEO analysis can be automated using Python by:

- Extracting webpage content programmatically
- Cleaning and processing textual data
- Identifying important keywords
- Structuring SEO insights into JSON format

This project is intended as a learning and workflow demonstration tool rather than a production-grade SEO software.

---

## ⚙️ How It Works

1. User provides a target webpage URL
2. HTML content is fetched using HTTP requests
3. Visible text is extracted from the page
4. Stopwords and irrelevant terms are removed
5. Keyword frequency scoring is applied
6. Results are exported as structured JSON output

---

## 🧰 Tech Stack

- Python
- Requests
- BeautifulSoup
- JSON
- Basic Text Processing

---

## 📦 Features

- URL-based content extraction
- Keyword frequency analysis
- Service keyword identification
- Structured JSON output
- Lightweight and easy to customize

---

## ⚠️ Limitations

- Uses frequency-based scoring only
- Does not include semantic keyword analysis
- No TF-IDF or NLP model integration
- Built mainly for learning automation workflow

---

## 🚀 Future Improvements

- Keyword density calculation
- Heading tag analysis (H1, H2, H3)
- Meta title & description extraction
- TF-IDF scoring
- Semantic keyword clustering

---

## ▶️ How to Run

1. Clone this repository

