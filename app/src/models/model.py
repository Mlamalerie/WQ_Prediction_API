import joblib
from enum import Enum
import os
import json


class ModelName(str, Enum):
    randomforest = "RF Regressor"
    linear = "Linear Regressor"


class ModelManager():
    """
    name: str
    model : RandomForestClassifier
    model_path : str
    data_path : str
    metrics: dict
    metrics_path : str
    parameters : dict"""

    def __init__(self, name: ModelName, model_path: str, data_path: str, metrics_path: str):
        self.name = name

        self.model_path = model_path
        self.data_path = data_path
        self.metrics_path = metrics_path

        self.model = None
        self.metrics = None
        self.parameters = None

        self.load_model(model_path)


    def load_model(self, model_path):
        """ load the model from the pkl file
        Args:
            model_path (str): path of the pkl file
        """
        #if os.path.exists(model_path):
        #    print(model_path) #todo : delete
        self.model = joblib.load(model_path)

    def get_parameters(self):
        """ get the parameters of the model
        """
        if not self.parameters:
            self.parameters = self.model.get_params()
            return self.parameters
        return self.parameters

    def save_model(self, model_output_filepath: str, metrics_output_filepath: str):
        """ save the model in a pkl file
        Args:
            model_output_filepath (str): path of the pkl file
        """
        if self.model:
            joblib.dump(model, model_output_filepath)
            json.dump(self.metrics, open(metrics_output_filepath, "w"))

    def get_metrics(self):
        """ get the metrics of the model
        """
        if not self.metrics:
            self.metrics = json.load(open(self.metrics_path, "r"))
            return self.metrics
        return self.metrics
