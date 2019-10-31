import warnings

from sklearn.exceptions import UndefinedMetricWarning

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
from sklearn.metrics import precision_recall_fscore_support
from experiments.results import add_result
from experiments.persist_model import load_params, persist_params
from sklearn.model_selection import GridSearchCV
from experiments.pipelines import classifiers
from experiments.data import get_train_test_split


CATEGORIES = ['category_1',
              'category_2',
              'category_3',
              'category_4',
              'category_5',
              'category_6',
              'category_7',
              'category_8',
              'category_9',
              'category_10',
              'category_9999',]


def evaluate(x_train, x_test, y_train, classifier, classification_name):
    clsf = classifiers[classifier][0]
    pipeline = classifiers[classifier][1]
    param_grid = classifiers[classifier][2]

    if classifier != 'ANN-BOW':
        params = load_params(classification_name)
        # set the classifier
        pipeline.set_params(clf=clsf)

        if not params:
            gs_cv = GridSearchCV(estimator=pipeline, param_grid=param_grid, cv=5, n_jobs=-1,
                                 scoring='recall', verbose=1)
            gs_cv.fit(x_train, y_train)
            # set the best classifier and persist it
            persist_params(gs_cv.best_params_, classification_name)
            params = gs_cv.best_params_
            print("Best: %f using %s" % (gs_cv.best_score_, gs_cv.best_params_))

        pipeline.set_params(**params)
        pipeline.fit(x_train, y_train)
        predicted = pipeline.predict(x_test)
    else:
        # fit the vectorizer to get the vocab size
        pipeline['vect'].fit(x_train, y_train)
        vocab_size = len(pipeline['vect'].get_feature_names())
        # set the classifier
        input_dim={'clf__input_dim': vocab_size}
        pipeline.set_params(clf=clsf)
        pipeline.set_params(**input_dim)
        pipeline.fit(x_train, y_train)
        predicted = pipeline.predict(x_test)

    return predicted


def main():
    for classifier in classifiers.keys():
        for category in CATEGORIES:
            print('Running {} for {}'.format(classifier, category))
            x_train, x_test, y_train, y_test = get_train_test_split(category)
            predicted = evaluate(x_train, x_test, y_train, classifier, '{}-{}'.format(classifier, category))
            precision, recall, f1, support = precision_recall_fscore_support(y_test, predicted, average='binary')
            add_result('results/results.csv', category, classifier, precision, recall, f1)


if __name__ == '__main__':
    main()
