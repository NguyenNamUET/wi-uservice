import os
import functools
import connexion
from sklearn import metrics
from sklearn.model_selection import train_test_split

from src import ml_models
from src import config


def parse_body_request(func):
    @functools.wraps(func)
    def modified_func(*args, **kwargs):
        request_body = connexion.request.json
        if request_body:
            if func.__name__ not in ["train", "predict", "create", "push", "delete", "train_by_bucket_data"]:
                # seperate model_type and parameters 
                kwargs.update(parameters=request_body)
            else:
                kwargs.update(request_body)
        return func(*args, **kwargs)
    return modified_func


def model_create(model_id, model_type, parameters):
    model_path = os.path.join(config.model_dir, model_id+'.joblib')

    # get definition validator
    validatorDefinition = ml_models.get_validator(model_type)
    # fit value
    validator = validatorDefinition(**parameters)
    # validate
    params = validator()
    model = ml_models.build_model(model_type, params)
    
    ml_models.save_model(model, model_path)


def model_train(model_id, features, target):
    result = {}
    model_path = os.path.join(config.model_dir, model_id+'.joblib')
    model = ml_models.load_model(model_path)

    #x_train, x_test, y_train, y_test = train_test_split(features, target)
    x_train, y_train = features, target
    x_test, y_test = features, target

    print(type(model))
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    result["mean_squared_error"] = metrics.mean_squared_error(y_test, y_pred)
    result["mean_absolute_error"] = metrics.mean_absolute_error(y_test, y_pred)
    ml_models.save_model(model, model_path)

    return result


def model_predict(model_id, features):
    model_path = os.path.join(config.model_dir, model_id+'.joblib')
    model = ml_models.load_model(model_path)
    target = model.predict(features)
    return target.tolist()

