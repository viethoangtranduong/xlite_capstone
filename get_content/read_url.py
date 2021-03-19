from newspaper import Article
# import nltk
# nltk.download('punkt')


def read_url(url):
    """read content from url

    Args:
        url (str): the content

    Returns:
        (str) the text in the url
    """    
    try:
        # use newspaper3k to scrape
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        text_out = article.text
    except:
        text_out = "ERROR!"

    return text_out