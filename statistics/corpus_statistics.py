import pandas as pd


def main():
    pd.set_option('display.max_columns', 30)
    pd.set_option('display.max_rows', None)
    annotations_path = '../data/annotations.csv'
    posts_path = '../data/posts.json'
    dataset_annotations = pd.read_csv(annotations_path, encoding='utf-8')
    dataset_posts = pd.read_json(posts_path, encoding='utf-8')

    dataset_annotations.set_index('post_id')
    dataset_posts.set_index('id')
    dataset_corpus = dataset_posts.join(dataset_annotations, how='inner')

    print(dataset_posts.head())

    # posts per page
    print(dataset_posts.groupby(['page_owner']).agg('count')['id'])

    # posts per type
    print(dataset_posts.groupby(['type']).agg('count')['id'])

    # posts per phase
    print(dataset_corpus.groupby(['phase']).agg('count')['id'])


if __name__ == '__main__':
    main()
