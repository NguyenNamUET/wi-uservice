from src.ml_models import result
from src.ml_models import validator
from typing import List, Dict
#from sklearn.base import BaseEstimator

from .k_nearest_neighbors_classifier_estimator import WiEstimator as KNearestNeighborsClassifierEstimator

KNearestNeighborsClassifierParameters = [
    {
        "name": "num_neighbors",
        "type": int
    },
    {
        "name": "p",
        "type": int
    },
    {
        "name": "metric",
        "type": str
    },
]

class KNearestNeighborsClassifierValidator(validator.BaseValidator):
    def __init__(self, **kwargs):
        self.props = KNearestNeighborsClassifierParameters
        validator.BaseValidator.doInit(self, **kwargs)

    def __call__(self):
        return_params = super(KNearestNeighborsClassifierValidator, self).__call__()
        # additional validation goes here
        return return_params

class KNearestNeighborsClassifierResult(result.SuccessResult):
    def __init__(self, *args, **kwargs):
        super(KNearestNeighborsClassifierResult, self).__init__()
        for key, value in kwargs.items():
            self.add(key, value)

# class KNearestNeighborsClassifierEstimator(WiEstimator):
  # Modify this class if you do not want to extend WiEstimator class
  # pass

