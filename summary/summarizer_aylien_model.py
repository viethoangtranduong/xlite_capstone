from aylienapiclient import textapi
from nltk import sent_tokenize
from nltk.tokenize import sent_tokenize


def summarizer_aylien_get(text, percent_sentences):

    num_sentences = int(percent_sentences / 100 * len(sent_tokenize(text)))


    output = {}

    client = textapi.Client("79e389d3", "1bc2400da0cb4745c30fb68b67e5e5cf")

    out = client.Summarize({'sentences_number': num_sentences,
                            'text': text,
                            'title': None})

    output['summary_num_sentences'] = num_sentences
    output['sentences'] = "".join([" " + val for val in out['sentences']])[1:]
    output['method'] = "Aylien"
    return output