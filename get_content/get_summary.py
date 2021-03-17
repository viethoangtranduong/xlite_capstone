from summary.summarizer_textrank_model import summarizer_textrank_get
from summary.summarizer_tfidf_model import summarizer_tfidf_get
from summary.summarizer_aylien_model import summarizer_aylien_get


def get_summary(text, percentage, method):
    if percentage == 0:
        return ""
    if percentage == 100:
        return text

    if method == "TextRank":
        return summarizer_textrank_get(text, percentage)

    elif method == "TF-IDF":
        return summarizer_tfidf_get(text, percentage)

    elif method == "Aylien":
        return summarizer_aylien_get(text, percentage)
    
    else:
        return {"sentences": "ERROR! No such method", "method": method}