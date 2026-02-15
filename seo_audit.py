import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import json

HEADERS = {"User-Agent": "Mozilla/5.0"}

# Core service indicators (expand per niche)
SERVICE_TERMS = {
    "tax", "accounting", "reporting", "analysis",
    "advisory", "planning", "consulting",
    "payroll", "bookkeeping", "financial",
    "compliance", "outsourcing", "audit"
}

# Junk/UI words
STOPWORDS = {
    "your", "for", "the", "and", "with", "our",
    "view", "detail", "learn", "more", "get",
    "new", "now", "click", "all", "about"
}

SECTION_WEIGHTS = {
    "title": 5,
    "h1": 4,
    "h2": 3,
    "h3": 2,
    "nav": 2,
    "li": 3,   # Services often listed here
    "body": 1
}


def fetch_html(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text


def clean_text(text):
    text = re.sub(r"[^a-zA-Z\s&]", " ", text.lower())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def valid_phrase(words):
    if len(words) < 2 or len(words) > 3:
        return False

    if any(w in STOPWORDS for w in words):
        return False

    if not any(term in words for term in SERVICE_TERMS):
        return False

    return True


def extract_weighted_phrases(text, weight, scores):
    text = clean_text(text)
    words = text.split()

    for i in range(len(words) - 1):
        phrase_words = words[i:i+2]
        if valid_phrase(phrase_words):
            phrase = " ".join(phrase_words)
            scores[phrase] += weight

        if i < len(words) - 2:
            phrase_words = words[i:i+3]
            if valid_phrase(phrase_words):
                phrase = " ".join(phrase_words)
                scores[phrase] += weight


def remove_overlapping_phrases(scores):
    phrases = sorted(scores.keys(), key=len)
    cleaned = {}

    for phrase in phrases:
        if not any(phrase in longer and phrase != longer for longer in cleaned):
            cleaned[phrase] = scores[phrase]

    return cleaned


def extract_keywords(url):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    scores = defaultdict(int)

    # Structured sections
    if soup.title:
        extract_weighted_phrases(soup.title.get_text(), SECTION_WEIGHTS["title"], scores)

    for level in ["h1", "h2", "h3"]:
        for tag in soup.find_all(level):
            extract_weighted_phrases(tag.get_text(), SECTION_WEIGHTS[level], scores)

    for li in soup.find_all("li"):
        extract_weighted_phrases(li.get_text(), SECTION_WEIGHTS["li"], scores)

    for nav in soup.find_all("nav"):
        extract_weighted_phrases(nav.get_text(), SECTION_WEIGHTS["nav"], scores)

    # Body
    body_text = soup.get_text(separator=" ")
    extract_weighted_phrases(body_text, SECTION_WEIGHTS["body"], scores)

    # Remove phrase explosion
    cleaned_scores = remove_overlapping_phrases(scores)

    sorted_keywords = sorted(cleaned_scores.items(), key=lambda x: x[1], reverse=True)

    result = {
        "url": url,
        "top_service_related_keywords": [
            {"keyword": k, "score": v}
            for k, v in sorted_keywords[:20]
        ]
    }

    return json.dumps(result, indent=4)


if __name__ == "__main__":
    user_url = input("Enter URL: ")
    print(extract_keywords(user_url))
