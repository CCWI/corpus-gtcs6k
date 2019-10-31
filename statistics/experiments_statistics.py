from collections import OrderedDict

import pandas as pd

from experiments.run import CATEGORIES


def min_greater_zero(a):
    a = [*a.values, float('inf')]
    print(a)
    greater = min(i for i in a if i > 0)
    print(greater)
    return greater


def print_table(df):
    classifiers = ['SVM-BOW','MNB-BOW','XGB-BOW','RF-BOW','ANN-BOW','RF-D2V']
    measures = OrderedDict([
        ['precision', 'Prec.'],
        ['recall', 'Rec.'],
        ['f1', '$F_1$']
    ])

    df_best = pd.DataFrame([[0 for x in classifiers] for x in measures],
                           index=measures, columns=classifiers)
    df_worst = pd.DataFrame([[0 for x in classifiers] for x in measures],
                           index=measures, columns=classifiers)
    df_none = pd.DataFrame([[0 for x in classifiers] for x in measures],
                           index=measures, columns=classifiers)

    grouped_df = df.groupby(['category', 'classifier'])
    table_df = grouped_df.agg('max')
    header = '\n'
    header+='\\begin{table}[ht]\n'
    header+='\centering\n'
    header+='\caption{Results of the baseline classification}\n'
    header+='\label{tab:results_classification}\n'
    header+='\\begin{tabular}{llcccccc}\n'
    header+='\\toprule\n'
    header+='& & \multicolumn{5}{c}{Bag of words} & D2V\\\\ \cmidrule{3-7}\cmidrule{8-8}\n'
    header+='Cat. & Meas. & SVM & MNB & XGB & RF & ANN & RF\\\\\n'
    header+='\midrule\n'

    body = ''
    for category in CATEGORIES:
        for meas in ['precision', 'recall', 'f1']:
            if meas == 'precision':
                cat = category.partition('_')[2]
                cat = str(11) if cat == str(9999) else cat
                body+='\multirow{3}{*}{' + cat + '.} & ' + \
                      '{}'.format(measures[meas])
            else:
                body+='& {} '.format(measures[meas])
            for alg in classifiers:
                # if none
                if table_df.loc[(category, alg), meas] == 0.0:
                    body += '& {:5.4f}'.format(
                        round(table_df.loc[(category, alg), meas], 4)
                    )
                    df_none.loc[meas, alg] += 1
                # if worst
                elif table_df.loc[(category, alg), meas] == min_greater_zero(table_df.loc[(category, classifiers), meas]):
                    body += '& \\textsl{'
                    body += '{:5.4f}'.format(
                        round(table_df.loc[(category, alg), meas], 4)
                    )
                    body += '}'
                    df_worst.loc[meas, alg] += 1
                # if best
                elif table_df.loc[(category, alg), meas] == max(table_df.loc[(category, classifiers), meas])\
                        and table_df.loc[(category, alg), meas] != min(table_df.loc[(category, classifiers), meas]):
                    body += '& \\textbf{'
                    body += '{:5.4f}'.format(
                        round(table_df.loc[(category, alg), meas], 4)
                    )
                    body += '}'
                    df_best.loc[meas, alg] += 1
                else:
                    body += '& {:5.4f}'.format(
                        round(table_df.loc[(category, alg), meas], 4)
                    )
            if meas == 'f1' and category != CATEGORIES[-1]:
                body+='\\\\[0.5em]\n'
            else:
                body += '\\\\\n'
    body+='\midrule\n'
    # none
    for meas in ['precision']:
        if meas == 'precision':
            body += 'None & ' + \
                    '{}'.format(measures[meas])
        else:
            body += '& {} '.format(measures[meas])
        for alg in classifiers:
            if df_none.loc[meas, alg] != max(df_none.loc[meas]) \
                    or df_none.loc[meas, alg] == min(df_none.loc[meas]):
                body += '& {}'.format(
                    df_none.loc[meas, alg]
                )
            else:
                body += '& \\textbf{'
                body += '{}'.format(
                    df_none.loc[meas, alg], 4
                )
                body += '}'
        body += '\\\\\n'
    body += '\midrule\n'
    # worst
    for meas in ['precision', 'recall', 'f1']:
        if meas == 'precision':
            body += '\multirow{3}{*}{Worst} & ' + \
                    '{}'.format(measures[meas])
        else:
            body += '& {} '.format(measures[meas])
        for alg in classifiers:
            if df_worst.loc[meas, alg] != max(df_worst.loc[meas]) \
                    or df_worst.loc[meas, alg] == min(df_worst.loc[meas]):
                body += '& {}'.format(
                    df_worst.loc[meas, alg]
                )
            else:
                body += '& \\textbf{'
                body += '{}'.format(
                    df_worst.loc[meas, alg], 4
                )
                body += '}'
        body += '\\\\\n'
    body += '\midrule\n'
    # best
    for meas in ['precision', 'recall', 'f1']:
        if meas == 'precision':
            body += '\multirow{3}{*}{Best} & ' + \
                    '{}'.format(measures[meas])
        else:
            body += '& {} '.format(measures[meas])
        for alg in classifiers:
            if df_best.loc[meas, alg] != max(df_best.loc[meas]) \
                    or df_best.loc[meas, alg] == min(df_best.loc[meas]):
                body += '& {}'.format(
                    df_best.loc[meas, alg]
                )
            else:
                body += '& \\textbf{'
                body += '{}'.format(
                    df_best.loc[meas, alg], 4
                )
                body += '}'
        body += '\\\\\n'

    footer = ''
    footer+='\\bottomrule\n'
    footer+='\end{tabular}\n'
    footer+='\end{table}\n'

    print(header+body+footer)

def main():
    pd.set_option('display.max_columns', 30)
    pd.set_option('display.max_rows', 1000)
    results_path = '../experiments/results/results.csv'
    posts_path = '../data/posts.json'
    dataset_results = pd.read_csv(results_path, encoding='utf-8')

    print(dataset_results.head())

    # posts per page
    grouped_df = dataset_results.groupby(['category', 'classifier'])

    # display the values
    print(grouped_df.agg('max').loc[('category_2', 'SVM-BOW'), 'precision'])

    print(grouped_df.agg('max').loc[('category_1', ['SVM-BOW','MNB-BOW','XGB-BOW','RF-BOW','ANN-BOW','RF-D2V']), 'precision'])
    print(max(grouped_df.agg('max').loc[('category_1', ['SVM-BOW','MNB-BOW','XGB-BOW','RF-BOW','ANN-BOW','RF-D2V']), 'precision']))

    print_table(dataset_results)


if __name__ == '__main__':
    main()
