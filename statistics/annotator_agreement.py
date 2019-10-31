from statistics import mean

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nltk import agreement


def multi_kappa(data):
    ratingtask = agreement.AnnotationTask(data=data)
    return ratingtask.multi_kappa()


def calculate_kappe(data, from_date, to_date, name):
    print('Calculating annotator agreement from {} to {}'.format(from_date, to_date))

    df2 = data

    df2['created_time'] = df2['created_time'].apply(pd.to_datetime)
    df2 = df2[(df2['created_time'] >= from_date) & (df2['created_time'] <= to_date)]

    number_of_annotators = len(df2.groupby('user_id'))
    annotators = range(1, number_of_annotators+1)

    print('Number of annotations: {}'.format(len(df2)))
    print('Posts per Annotator: {}'.format(len(df2) / number_of_annotators))
    print('')

    values = list()
    values_formatted = list()

    categories = ["category_1", "category_2", "category_3", "category_4", "category_5", "category_6", "category_7",
                  "category_8", "category_9", "category_10", "category_9999"]
    category_labels = ['Success', 'All Topics', '1. Product/Service', '2. Event/Fair', '3. Interactions', '4. News', '5. Entertainment', '6. Knowledge',
                       '7. Recruiting/HR', '8. Corporate Social\n Responsibility', '9. Advertising/Campaign', '10. Sponsoring',
                       '11. Other']

    for category in categories:
        category_df = df2.filter(items=['user_id', 'post_id', category])
        category_data = category_df.values.tolist()
        try:
            rating = multi_kappa(category_data)
            values.append(rating)
            values_formatted.append('{}: {}'.format(category, rating))
        except ZeroDivisionError as e:
            values.append(0.0)
            # Suppress the exception
            # ZeroDivisionError occurs of no post for that class exists
            pass
    print('Kappa values: {}'.format(values))
    print('Kappa values: {}'.format(values_formatted))
    mean_rating = mean([x for x in values if x > 0])
    print('Kappa on category (mean): {}'.format(mean_rating))
    success_data = df2.filter(items=['user_id', 'post_id', 'successful']).values.tolist()
    success_rating = multi_kappa(success_data)
    print('Kappa on success: {}'.format(success_rating))
    print('')
    val_new = list()
    val_new.append(success_rating)
    val_new.append(mean_rating)
    for x in values:
        val_new.append(x)
    df3 = pd.DataFrame([val_new], columns=category_labels, index=['All'])

    for annotator in annotators:
        values_wo = list()
        for category in categories:
            category_df = df2.filter(items=['user_id', 'post_id', category])
            category_df = category_df[category_df['user_id'] != annotator]
            category_data = category_df.values.tolist()
            try:
                rating = multi_kappa(category_data)
                print('{} {}: '.format(category, rating))
                values_wo.append(rating)
            except ZeroDivisionError as e:
                values_wo.append(0.0)
                # Suppress the exception
                # ZeroDivisionError occurs of no post for that class exists
                pass
        print('Kappa values, without {}: {}'.format(annotator, values_wo))
        mean_rating_wo = mean([x for x in values_wo if x > 0])
        print('Kappa on category (mean), without {}: {}'.format(annotator, mean_rating_wo))
        success_df = df2.filter(items=['user_id', 'post_id', 'successful'])
        success_df = success_df[success_df['user_id'] != annotator]
        success_data = success_df.values.tolist()
        success_rating_wo = multi_kappa(success_data)
        print('Kappa on success, without {}: {}'.format(annotator, success_rating_wo))
        print('')
        val_new2 = list()
        val_new2.append(success_rating_wo)
        val_new2.append(mean_rating_wo)
        for x in values_wo:
            val_new2.append(x)
        df3 = df3.append(pd.DataFrame([val_new2], columns=category_labels, index=['Without {}'.format(annotator)]))
    print(df3)
    plot_horizontal(df3, name)


def plot_horizontal(data, plot_name):
    plt.rcdefaults()
    plt.style.use('grayscale')
    cm = plt.get_cmap('gist_gray')
    fig, ax = plt.subplots()
    co = iter(cm(np.linspace(0, 2, len(data.columns))))
    cols = [next(co), next(co),next(co),next(co),next(co),next(co)]
    y_pos = 5*np.arange(len(data.columns))
    width = 0.75

    rects1 = ax.barh(y_pos - 2.5*width, data.iloc[0], width, align='center', label='All Experts', color=cols[0])
    rects2 = ax.barh(y_pos - 1.5*width, data.iloc[1], width, align='center', label='Without 1', color=cols[4])
    rects3 = ax.barh(y_pos - 0.5*width, data.iloc[2], width, align='center', label='Without 2', color=cols[2])
    rects4 = ax.barh(y_pos + 0.5*width, data.iloc[3], width, align='center', label='Without 3', color=cols[5])
    rects5 = ax.barh(y_pos + 1.5*width, data.iloc[4], width, align='center', label='Without 4', color=cols[1])
    rects6 = ax.barh(y_pos + 2.5*width, data.iloc[5], width, align='center', label='Without 5', color=cols[3])

    ax.set_yticks(y_pos)
    ax.set_yticklabels(data.columns)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Fleiss\' Kappa')
    ax.legend()

    plt.show()
    for plot_format in ['eps', 'pdf', 'png']:
        fig.savefig('plots/annotator_agreement_{}.{}'.format(plot_name, plot_format), dpi=fig.dpi, bbox_inches = "tight")


def main():
    annotations_path = '../data/annotations.csv'
    dataset = pd.read_csv(annotations_path)

    df2 = dataset[dataset['phase'] == 2]

    calculate_kappe(df2, '2000-01-01', '2019-05-31', 'a')
    calculate_kappe(df2, '2019-06-03', '2099-12-31', 'b')


if __name__ == '__main__':
    main()
