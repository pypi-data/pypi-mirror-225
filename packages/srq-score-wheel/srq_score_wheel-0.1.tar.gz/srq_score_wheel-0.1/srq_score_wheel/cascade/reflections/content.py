"""This module is to standardize and clean the content column before creating features"""
import re
import unicodedata
import contractions
import inflect
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer


def extract_edited_content(content):
    """Applying all the modifications on the column sequentially"""
    return [
        normalize(
            stem_and_lemmatize(
                denoise_text(
                    replace_contractions(x)))) for x in content.replace("'", '')]


def strip_html(text):
    return BeautifulSoup(text, "html.parser").get_text()


def remove_between_square_brackets(text):
    return re.sub(r'\[[^]]*\]', '', text)


def denoise_text(text):
    return (remove_between_square_brackets(strip_html(text)).
            replace("i'll", 'i will').
            replace("i'm", 'i am'))


def replace_contractions(string_with_numbers):
    return contractions.fix(str(string_with_numbers))


def remove_non_ascii(words):
    return ([unicodedata.normalize('NFKD', word).
             encode('ascii', 'ignore').
             decode('utf-8', 'ignore') for word in words])


def to_lowercase(words):
    return [word.lower() for word in words]


def remove_punctuation(words):
    # replace multiple spaces with one
    return [re.sub(r'\s{2,}', ' ',
                   # adds spaces next to each punctuation, separating words around
                   (re.sub('([.,!?])', r' \1 ',
                           # removing puctuations
                           (re.sub(r'[^\w\s]', '', word))))) for word in words if word != '']


def replace_numbers(words):
    """Replace all integer occurrences in list of tokenized words with textual representation"""
    return [num_words(word) if word.isdigit() else word for word in words]

# pylint: disable=W0702
# No exception type(s) specified
def num_words(word):
    try:
        return inflect.engine().number_to_words(word)
    except:
        return word


def remove_stopwords(words):
    return [word for word in words if word not in stopwords.words('english')]


def stem_words(words):
    return [LancasterStemmer().stem(x) for x in words]


def lemmatize_verbs(words):
    return [WordNetLemmatizer().lemmatize(x, pos='v') for x in words]


def normalize(sample):
    words = replace_numbers(
        to_lowercase(
            remove_non_ascii(
                remove_punctuation(
                    nltk.word_tokenize(sample)))))
    return TreebankWordDetokenizer().detokenize(words)


def stem_and_lemmatize(sample):
    return TreebankWordDetokenizer().detokenize(lemmatize_verbs(nltk.word_tokenize(sample)))
