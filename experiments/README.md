# Experiments
In this folder we provide the experiments for the corpus on German topic classification and success (GTCS6k). Please see the [corpus website](https://ccwi.github.io/corpus-gtcs6k/) for more information about the corpus.

## Requirements
All packages required to run the experiments are stored in the `requirements.txt` file. 

Please create a new virtual environment and run `pip install -r requirements.txt` to install the packages.

## How to run the experiments?
In order to run the experiments, the following programs have to be executed in the given order:

````python
train_doc2vec.py
run.py
````

After the execution is complete, the results can be found in the file `results/results.csv`.
 