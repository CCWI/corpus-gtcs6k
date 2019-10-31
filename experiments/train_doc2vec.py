from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from sklearn import utils as skl_utils
from tqdm import tqdm

from experiments.data import get_unannotated_posts, get_train_test_split
from experiments.preprocessing import tokenize

if __name__ == '__main__':
    # Use the training set together with the unannotated posts to train the vector
    x_train, x_test, y_train, y_test = get_train_test_split('category_1')
    unannotated_posts = get_unannotated_posts()
    df_x = x_train.append(unannotated_posts['text'])

    learning_rate = 0.02
    epochs = 20

    tagged_x = [TaggedDocument(tokenize(row), [index]) for index, row in enumerate(df_x)]

    for vector_size in [100, 200, 300]:
        model = Doc2Vec(documents=tagged_x, vector_size=vector_size, workers=-1)

        for epoch in range(epochs):
            model.train(skl_utils.shuffle([x for x in tqdm(tagged_x)]), total_examples=len(tagged_x), epochs=1)
            model.alpha -= learning_rate
            model.min_alpha = model.alpha

        model.save("models/doc2vec/doc2vec_{}.model".format(vector_size))
