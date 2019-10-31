from collections import OrderedDict

import xgboost as xgb
from keras.layers import Dense
from keras.models import Sequential
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from experiments.Doc2VecTransformer import Doc2VecTransformer
from experiments.preprocessing import tokenize

bow_pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('clf', None),
        ])

tfidf_pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', None),
        ])

d2v_pipeline = Pipeline([
        ('doc2vec', Doc2VecTransformer()),
        ('clf', None),
        ])


def _get_param_grid_cv():
        return {
        'vect__ngram_range': [(1, 1)] #[(1, 1), (1, 2), (1, 3)]
        }


def _get_param_grid_rf():
        return {
        #'clf__n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000],
        #'clf__max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None]
        }


def get_param_grid_svm_bow():
        data = _get_param_grid_cv()
        data.update({
                'clf__max_iter': [3000]
        })
        return data


def get_param_grid_mnb_bow():
        data = _get_param_grid_cv()
        data.update({

        })
        return data


def get_param_grid_xgb_bow():
        data = _get_param_grid_cv()
        data.update({

        })
        return data


def get_param_grid_rf_bow():
        data = _get_param_grid_cv()
        data.update(_get_param_grid_rf())
        return data


def get_param_grid_rf_d2v():
        data = {
                'doc2vec__vector_size': [x for x in range(100, 300, 100)]
        }
        data.update(_get_param_grid_rf())
        return data


def get_param_grid_ann_bow():
        data = _get_param_grid_cv()
        data.update({

        })
        return data


def create_baseline(input_dim):
    # create model
    model = Sequential()
    model.add(Dense(23, kernel_initializer='normal', activation='relu', input_dim=input_dim))
    model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


classifiers = OrderedDict([
    [ 'SVM-BOW', [LinearSVC(), bow_pipeline, get_param_grid_svm_bow()] ],
    [ 'MNB-BOW', [MultinomialNB(), bow_pipeline, get_param_grid_mnb_bow()] ],
    [ 'XGB-BOW', [xgb.XGBClassifier(), bow_pipeline, get_param_grid_xgb_bow()] ],
    [ 'RF-BOW', [RandomForestClassifier(n_estimators=100), bow_pipeline, get_param_grid_rf_bow()] ],
    [ 'RF-D2V', [RandomForestClassifier(n_estimators=100), d2v_pipeline, get_param_grid_rf_d2v()] ],
    [ 'ANN-BOW', [KerasClassifier(build_fn=create_baseline, epochs=100, batch_size=10, verbose=1),
                  bow_pipeline, get_param_grid_ann_bow() ] ],
])
