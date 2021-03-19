import math
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords  
import numpy as np
  
# extracting from https://github.com/bhuwanesh340/Text_Summarization_NLP/blob/master/Text_Summary.py
    
'''
We already have a sentence tokenizer, so we just need 
to run the sent_tokenize() method to create the array of sentences.
'''

def _create_frequency_matrix(sentences):
    """get frequency matrix for words

    Args:
        sentences (str): text

    Returns:
        frequency matrix
    """    
    frequency_matrix = {}
    stopWords = set(stopwords.words("english"))
    ps = PorterStemmer()

    # remove stopwords and build a frequency matrix
    # if word not there, add to dictionary
    # if it's there, then add +1 to that value
    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            word = ps.stem(word)
            if word in stopWords:
                continue
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:15]] = freq_table

    return frequency_matrix


def _create_tf_matrix(freq_matrix):
    """get term frequency

    Args:
        frequency matrix (dict)

    Returns:
        term frequency matrix
    """      
    tf_matrix = {}

    # frequency divide by length of document
    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix


def _create_documents_per_words(freq_matrix):
    """create documents for each word

    Args:
        frequency matrix (dict)

    Returns:
        document per word
    """      
    word_per_doc_table = {}

    # start counting 
    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table


def _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
    """iv=nverse document frequency

    Args:
        freq_matrix (dict): frequency
        count_doc_per_words (dict): document frequency
        total_documents (int): number of documents

    Returns:
        inverse document frequency matrix
    """    
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        # follow the formula
        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix


def _create_tf_idf_matrix(tf_matrix, idf_matrix):
    """tf-idf matrix from tf and idf matrices

    Args:
        tf_matrix (dict): term frequency
        idf_matrix (dict):document frequency

    Returns:
        dict: tf-idf matrix
    """    
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):  # here, keys are the same in both the table
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix


def _score_sentences(tf_idf_matrix) -> dict:
    """score a sentence by its word's TF: adding the TF frequency of 
    every non-stop word in a sentence divided by total no of words in a sentence.

    Args:
        tf_idf_matrix (dict): tf-idf values above

    Returns:
        dict: each sentence value
    """    

    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score
        # formula
        sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence

    return sentenceValue


def _find_score(sentenceValue, percent_sentences) -> int:
    """Find the average score from the sentence value dictionary

    Args:
        sentenceValue (dict): sentences' values above 
        percent_sentences (int): percent of information to retain

    Returns:
        int: threshold to keep
    """   

    values = []
    for entry in sentenceValue:
        values.append(sentenceValue[entry])

    # Average value of a sentence from original summary_text
    return np.percentile(values, 100 - percent_sentences)


def _generate_summary(sentences, sentenceValue, threshold):
    """get the summary: if value above the threshold

    Args:
        sentences (list): all sentences
        sentenceValue (dict): the dict storing its value
        threshold (int): threshold to select sentences

    Returns:
        (str): summary
    """    
    sentence_count = 0
    summary = ''

    # check if qualify 
    for sentence in sentences:
        if sentence[:15] in sentenceValue and sentenceValue[sentence[:15]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary


def summarizer_tfidf_get(text, percent_sentences = 50):
    """sumarize using tfidf

    Args:
        text (str): the text to summarize
        percent_sentences (int, optional): percent to retain. Defaults to 50.

    Returns:
        (str) summarized summary_text
    """ 

    sentences = sent_tokenize(text)

    # 1 Sentence Tokenize
    
    total_documents = len(sentences)
    #print(sentences)

    # 2 Create the Frequency matrix of the words in each sentence.
    freq_matrix = _create_frequency_matrix(sentences)
    #print(freq_matrix)

    '''
    Term frequency (TF) is how often a word appears in a document, divided by how many words are there in a document.
    '''
    # 3 Calculate TermFrequency and generate a matrix
    tf_matrix = _create_tf_matrix(freq_matrix)
    #print(tf_matrix)

    # 4 creating table for documents per words
    count_doc_per_words = _create_documents_per_words(freq_matrix)
    #print(count_doc_per_words)

    '''
    Inverse document frequency (IDF) is how unique or rare a word is.
    '''
    # 5 Calculate IDF and generate a matrix
    idf_matrix = _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents)
    #print(idf_matrix)

    # 6 Calculate TF-IDF and generate a matrix
    tf_idf_matrix = _create_tf_idf_matrix(tf_matrix, idf_matrix)
    #print(tf_idf_matrix)

    # 7 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(tf_idf_matrix)
    #print(sentence_scores)

    # 8 Find the threshold
    threshold = _find_score(sentence_scores, percent_sentences)
    #print(threshold)

    # 9 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, threshold)
    sentences = sent_tokenize(summary)

    # output
    output = {'sentences': summary, 'summary_num_sentences': len(sentences), "method": "tfidf"}

    return output