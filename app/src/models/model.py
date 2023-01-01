import time

import joblib
from enum import Enum
import os
import json

import numpy as np
import pandas as pd
from typing import Tuple, List

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder

from app.src.models.wine import Wine, WineLabelised


class ModelName(str, Enum):
    randomforest = "RFRegressor"
    linear = "LinearRegressor"


class DatasetManager():
    def __init__(self, file_path: str = "./app/datasource/datasets/Wines.csv"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} not found")
        self.base_dataset = pd.read_csv(self.file_path)
        # replace colunm names with lower case
        self.base_dataset.columns = self.base_dataset.columns.str.lower()
        name, ext = os.path.splitext(self.file_path)
        self.added_data_path = name + "_added" + ext

    def get_base_df_dataset(self) -> pd.DataFrame:
        return self.base_dataset

    def get_added_df_dataset(self) -> pd.DataFrame:
        return (
            pd.read_csv(self.added_data_path)
            if os.path.exists(self.added_data_path)
            else pd.DataFrame()
        )

    def get_dataset(self) -> pd.DataFrame:
        if os.path.exists(self.added_data_path):
            return pd.concat([self.base_dataset, self.get_added_df_dataset()], ignore_index=True)
        return self.base_dataset

    def get_base_wines(self) -> List[WineLabelised]:
        return self.base_dataset.to_dict(orient="records")

    def get_added_wines(self) -> List[WineLabelised]:
        return self.get_added_df_dataset().to_dict(orient="records")

    def get_wine_by_id(self, index: int) -> WineLabelised:
        return self.base_dataset.iloc[index].to_dict()

    def append_wine(self, wine: WineLabelised) -> Tuple[WineLabelised, List[Wine], bool]:
        wines_added = self.get_added_wines()
        wine_dict = wine.dict()
        if wine_dict in wines_added:
            return wine_dict, wines_added, False
        wines_added.append(wine_dict)
        self.base_dataset = pd.DataFrame(wines_added)
        self.base_dataset.to_csv(self.added_data_path, index=False)
        return wine_dict, wines_added, True


class ModelManager():
    """
    name: str
    model : RandomForestClassifier
    model_path : str
    data_path : str
    metrics: dict
    metrics_path : str
    parameters : dict"""

    def __init__(self, name: ModelName):
        self.name = name

        match name:
            case ModelName.randomforest:
                model_filename = "randomforestregressor.pkl"
                metrics_filename = "metrics_rf.json"
            case ModelName.linear:
                model_filename = "linearregression.pkl"
                metrics_filename = "metrics_lin.json"

        self.model_path = f"./app/datasource/predictors/{model_filename}"
        self.dataset_manager: DatasetManager = DatasetManager()
        self.metrics_path = f"./app/datasource/predictors/{metrics_filename}"
        self.added_data_path = None
        for path in [self.model_path, self.metrics_path]:
            if not os.path.exists(path):
                raise ValueError(f"Path '{path}' not exists... Please check the path")

        self.model = None
        self.metrics: dict = {}
        self.parameters: dict = {}

        self.load_model(self.model_path)

    def load_model(self, model_path):
        """ load the model from the pkl file
        Args:
            model_path (str): path of the pkl file
        """
        # if os.path.exists(model_path):
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

    def __preprocessing(self, df_wines: pd.DataFrame, test_size=0.2) -> pd.DataFrame:
        """ preprocessing of the dataset
        Args:
            df (pd.DataFrame): dataset
        """
        df = df_wines.copy()
        # drop columns
        if "Id" in df.columns:
            df = df.drop("Id", axis=1)

        # preprocess
        X = df.drop('quality', axis=1).values
        y = df['quality'].values

        my_pipeline = Pipeline([
            ('imputer', SimpleImputer()),
            ('scaler', StandardScaler())
        ])

        X = my_pipeline.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)

        return X_train, X_test, y_train, y_test

    def train(self, save_model: bool = True):
        """ train the model

        """
        # start timer
        start_time = time.time()
        # get dataset
        df_wines = self.dataset_manager.get_dataset()
        X_train, X_test, y_train, y_test = self.__preprocessing(df_wines)

        if not self.model:
            raise ValueError("Model not initialized")

        # train the model

        self.model.fit(X_train, y_train)

        # evaluate the model
        match self.name:
            case ModelName.randomforest:
                pass
            case ModelName.linear:
                pass

        self.metrics["score_train"] = self.model.score(X_train, y_train)

        self.metrics["score_test"] = self.model.score(X_test, y_test)
        y_predict_rfr = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_predict_rfr)
        rmse = np.sqrt(mse)
        self.metrics["rmse"] = rmse

        if save_model:
            self.save_model(self.model_path, self.metrics_path)

        # end timer
        end_time = time.time()
        self.metrics["time"] = end_time - start_time

        return len(X_train), len(X_test)

    def predict(self, wine: Wine) -> float:
        """ predict the quality of a wine
        Args:
            wine (Wine): wine to predict
        Returns:
            float: quality of the wine
        """
        if not self.model:
            raise ValueError("Model not initialized")

        X = np.array(list(wine.__dict__.values()))  # todo : check if it works, if not, use

        return self.model.predict([X])[0]
