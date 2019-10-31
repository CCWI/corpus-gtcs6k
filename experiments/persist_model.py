import joblib
from pathlib import Path
from keras.models import load_model


def persist_params(params, model):
    full_path = 'models/{}.pkl'.format(model)
    joblib.dump(params, full_path, compress=1)


def load_params(model):
    full_path = 'models/{}.pkl'.format(model)
    model = Path(full_path)
    if model.is_file():
        return joblib.load(full_path)
    return None


def persist_model(model, model_name):
    model.save('models/{}.pkl'.format(model_name))


def load_model(model):
    return load_model(model)
