import pandas as pd


def main():
    pd.set_option('display.max_columns', 30)
    annotations_path = '../data/annotations.csv'
    dataset = pd.read_csv(annotations_path)
    posts_per_pase = dataset.groupby(['phase', 'user_id']).agg('count')
    print(posts_per_pase['post_id'])


if __name__ == '__main__':
    main()
