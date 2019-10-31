import string
from nltk.tokenize.casual import TweetTokenizer

def tokenize(text):
    tweet_tokenizer = TweetTokenizer()
    # 1. Tokenize
    text = tweet_tokenizer.tokenize(text)
    # 2. Cleaning
    # Punctuation
    text = [t for t in text if t not in string.punctuation]
    # Normalisieren
    text = [t.lower() for t in text]
    return text
