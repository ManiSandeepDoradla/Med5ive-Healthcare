from typing import List, Tuple, Optional
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")
class TextProcessing:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words("english"))
 
    def remove_punctuations(self, text: str) -> str:
        return text.translate(str.maketrans("", "", string.punctuation))
 
    def tokenize(self, text: str) -> List[str]:
        return word_tokenize(text)
 
    def lemmatize(self, tokens: List[str]) -> List[str]:
        return [self.lemmatizer.lemmatize(tok) for tok in tokens]
 
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        return [tok for tok in tokens if tok not in self.stopwords]
 
    def preprocess_tokens(self, text: str) -> List[str]:
        text = self.remove_punctuations(text)
        text = text.lower().strip()
        tokens = self.tokenize(text)
        tokens = self.lemmatize(tokens)
        tokens = self.remove_stopwords(tokens)
        return tokens
 
    def preprocess_text(self, text: str) -> str:
        return " ".join(self.preprocess_tokens(text))