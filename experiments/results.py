from pathlib import Path
import pandas as pd

columns = ['category', 'classifier', 'precision', 'recall', 'f1']


def load_results(path):
    my_file = Path(path)
    if not my_file.exists():
        df = pd.DataFrame(columns=columns)
        df.to_csv(path, index=False)
    df = pd.read_csv(path)
    return df


def write_results(path, df):
    df.to_csv(path, index=False)


def add_result(path, category, classifier, precision, recall, f1):
    dataframe = load_results(path)
    dataframe = dataframe.append(
        pd.Series(
            [category, str(classifier), precision, recall, f1],
            index=dataframe.columns),
        ignore_index=True)
    write_results(path, dataframe)
