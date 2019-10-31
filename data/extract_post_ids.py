import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    posts_path = 'posts.json'
    dataset_posts = pd.read_json(posts_path, encoding='utf-8', dtype=False)
    print(dataset_posts.head())
    print(dataset_posts.info())
    post_ids = dataset_posts.filter(['id'])
    print(post_ids.head())
    post_ids['id'] = post_ids['id'].astype(str)
    post_ids.to_csv('post_ids.csv', sep=';', index=False)


if __name__ == '__main__':
    main()
