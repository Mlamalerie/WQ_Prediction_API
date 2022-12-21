import joblib
from enum import Enum
import os
import json
import pandas as pd
from typing import Tuple,List
from app.src.models.wine import Wine
class ModelName(str, Enum):
    randomforest = "RFRegressor"
    linear = "LinearRegressor"


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
        self.added_data_path = None
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

    def get_metrics(self):
        """ get the metrics of the model
        """
        if not self.metrics:
            self.metrics = json.load(open(self.metrics_path, "r"))
            return self.metrics
        return self.metrics

    def save_model(self, model_output_filepath: str, metrics_output_filepath: str):
        """ save the model in a pkl file
        Args:
            model_output_filepath (str): path of the pkl file
        """
        if self.model:
            joblib.dump(self.model, model_output_filepath)
            json.dump(self.metrics, open(metrics_output_filepath, "w"))


    def append_wine(self,wine : Wine) -> Tuple[Wine, List]:
        """ append a new wine to the dataset
        Args:
            wine (Wine): wine to append
        """
        name, ext = os.path.splitext(self.data_path)
        self.added_data_path = name + "_added" + ext

        if not os.path.exists(self.added_data_path):
            df_result = pd.DataFrame.from_records([wine.__dict__]) # create dataframe from wine
            df_result.to_csv(self.added_data_path, index=False) # save csv file
        else:
            df_to_add = pd.DataFrame.from_records([wine.__dict__])
            df_base = pd.read_csv(self.added_data_path) # read csv file
            df_result = pd.concat([df_base,df_to_add], ignore_index=True) # append wine
            df_result = df_result.drop_duplicates() # delete duplicates
            df_result.to_csv(self.added_data_path, index=False) # save csv file

        return wine,df_result.to_dict('records') # return wine and dataset #todo return list of wine ?

    def __preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        """ preprocessing of the dataset
        Args:
            df (pd.DataFrame): dataset
        """
        # todo : delete duplicate ligne
        pass



