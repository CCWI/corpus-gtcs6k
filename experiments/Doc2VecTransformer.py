from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from sklearn.base import BaseEstimator
from sklearn import utils as skl_utils
from tqdm import tqdm
from experiments.preprocessing import tokenize

import multiprocessing
import numpy as np

# Class from here: https://github.com/avisheknag17/public_ml_models/blob/master/bbc_articles_text_classification/notebook/text_classification_xgboost_others.ipynb


class Doc2VecTransformer(BaseEstimator):

    def __init__(self, vector_size=100, learning_rate=0.02, epochs=20):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self._model = None
        self.vector_size = vector_size
        self.workers = multiprocessing.cpu_count() - 1

    def fit(self, df_x, df_y=None):
        self._model = Doc2Vec.load("models/doc2vec/doc2vec_{}.model".format(self.vector_size))
        return self

    def transform(self, df_x):
        return np.asmatrix(np.array([self._model.infer_vector(tokenize(row))
                                     for index, row in enumerate(df_x)]))