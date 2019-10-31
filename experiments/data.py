import pandas as pd
from sklearn.model_selection import train_test_split


def get_annotated_posts():
    annotations_path = '../data/annotations.csv'
    posts_path = '../data/posts.json'
    dataset_annotations = pd.read_csv(annotations_path, encoding='utf-8')
    dataset_posts = pd.read_json(posts_path, encoding='utf-8')

    dataset_annotations.set_index('post_id')
    dataset_posts.set_index('id')
    dataset_corpus = dataset_posts.join(dataset_annotations, how='inner')
    return dataset_corpus[dataset_corpus['phase'] == 3]


def get_unannotated_posts():
    annotations_path = '../data/annotations.csv'
    posts_path = '../data/posts.json'
    dataset_annotations = pd.read_csv(annotations_path, encoding='utf-8')
    dataset_posts = pd.read_json(posts_path, encoding='utf-8')

    dataset_annotations.set_index('post_id')
    dataset_posts.set_index('id')
    dataset_corpus = dataset_posts.join(dataset_annotations, how='left')
    return dataset_corpus[dataset_corpus.category_1.isnull()]


def get_train_test_split(category):
    data = get_annotated_posts()
    return train_test_split(data['text'], data[category], test_size=0.33, random_state=42)
