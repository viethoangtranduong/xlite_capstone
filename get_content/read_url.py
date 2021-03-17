from newspaper import Article
import nltk
nltk.download('punkt')


def read_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        text_out = article.text
    except:
        text_out = "ERROR!"

    return text_out