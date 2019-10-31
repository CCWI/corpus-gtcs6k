import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    annotations_path = '../data/annotations.csv'
    dataset = pd.read_csv(annotations_path)
    phase_3 = dataset[dataset['phase'] == 3]
    posts_per_class = phase_3.agg({'category_1': ['sum', lambda x: round(x.sum()/phase_3['category_1'].count()*100, 2)],
                                   'category_2': ['sum', lambda x: round(x.sum()/phase_3['category_2'].count()*100, 2)],
                                   'category_3': ['sum', lambda x: round(x.sum()/phase_3['category_3'].count()*100, 2)],
                                   'category_4': ['sum', lambda x: round(x.sum()/phase_3['category_4'].count()*100, 2)],
                                   'category_5': ['sum', lambda x: round(x.sum()/phase_3['category_5'].count()*100, 2)],
                                   'category_6': ['sum', lambda x: round(x.sum()/phase_3['category_6'].count()*100, 2)],
                                   'category_7': ['sum', lambda x: round(x.sum()/phase_3['category_7'].count()*100, 2)],
                                   'category_8': ['sum', lambda x: round(x.sum()/phase_3['category_8'].count()*100, 2)],
                                   'category_9': ['sum', lambda x: round(x.sum()/phase_3['category_9'].count()*100, 2)],
                                   'category_10': ['sum', lambda x: round(x.sum()/phase_3['category_10'].count()*100, 2)],
                                   'category_9999': ['sum', lambda x: round(x.sum()/phase_3['category_9999'].count()*100, 2)]})

    posts_per_class = posts_per_class.rename(index={'<lambda>': 'percent'})

    values = posts_per_class.loc['percent']
    labels = ['Product/Service', 'Event/Fair', 'Interactions', 'News', 'Entertainment', 'Knowledge', 'Recruiting/HR',
              'Corporate Social\n Responsibility', 'Advertising/Campaign', 'Sponsoring', 'Other']
    name = 'class_distribution'
    plot_barplot(values, labels, name)

    posts_per_class_transponded = posts_per_class.T
    posts_per_class_transponded.index = labels
    posts_per_class_transponded.columns = ['Posts', 'Percent']
    print(posts_per_class_transponded)
    print(posts_per_class_transponded.to_html())
    posts_per_class_transponded.to_csv('calculations/posts_per_class.csv', sep=';')

    g = phase_3['successful']
    posts_per_success_rating = pd.concat([g.value_counts(), g.value_counts(normalize=True).mul(100)],
                                         axis=1, keys=('Posts', 'Percent'))

    posts_per_success_rating.index = ['Not successful', 'Successful']
    print(posts_per_success_rating)


def plot_barplot(values, labels, name):
    plt.rcdefaults()
    plt.style.use('grayscale')
    fig, ax = plt.subplots()

    y_pos = np.arange(len(labels))

    ax.barh(y_pos, values, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Percentage')
    # ax.set_title('Distribution of categories')

    plt.show()
    for plot_format in ['eps', 'pdf', 'png']:
        fig.savefig('plots/{}.{}'.format(name, plot_format), dpi=fig.dpi, bbox_inches="tight")


if __name__ == '__main__':
    main()
