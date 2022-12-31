import joblib
from enum import Enum
import os
import json
import pandas as pd
from typing import Tuple, List

from sklearn.ensemble import RandomForestClassifier
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
        name, ext = os.path.splitext(self.file_path)
        self.added_data_path = name + "_added" + ext

    def get_base_dataset(self) -> pd.DataFrame:
        return self.base_dataset

    def get_added_data(self) -> pd.DataFrame:
        if not os.path.exists(self.added_data_path):
            return pd.DataFrame()
        return pd.read_csv(self.added_data_path)

    def get_dataset(self) -> pd.DataFrame:
        if os.path.exists(self.added_data_path):
            return pd.concat([self.base_dataset, self.get_added_data()], ignore_index=True)
        return self.base_dataset

    def get_base_wines(self) -> List[WineLabelised]:
        return self.base_dataset.to_dict(orient="records")

    def get_added_wines(self) -> List[WineLabelised]:
        return self.get_added_data().to_dict(orient="records")

    def get_base_wine(self, index: int) -> WineLabelised:
        return self.base_dataset.iloc[index].to_dict()

    def append_wine(self, wine: WineLabelised) -> Tuple[WineLabelised, List[Wine], bool]:
        wines_added = self.get_added_wines()
        wine_dict = wine.dict()
        # check if wine already exists
        if wine_dict not in wines_added:
            wines_added.append(wine_dict)
            self.base_dataset = pd.DataFrame(wines_added)
            self.base_dataset.to_csv(self.added_data_path, index=False)
            return wine_dict, wines_added, True
        else:
            return wine_dict, wines_added, False

    def append_wine2(self, wine: Wine) -> Tuple[Wine, List]:
        """ append a new wine to the dataset
        Args:
            wine (Wine): wine to append
        """
        name, ext = os.path.splitext(self.file_path)
        self.added_data_path = name + "_added" + ext
        is_added = False
        if not os.path.exists(self.added_data_path):
            df_result = pd.DataFrame.from_records([wine.__dict__])  # create dataframe from wine
            if df_result.to_csv(self.added_data_path, index=False):  # save csv file
                is_added = True
        else:
            df_to_add = pd.DataFrame.from_records([wine.__dict__])
            df_base = pd.read_csv(self.added_data_path)  # read csv file
            df_result = pd.concat([df_base, df_to_add], ignore_index=True)  # append wine
            df_result = df_result.drop_duplicates()  # delete duplicates
            df_result.to_csv(self.added_data_path, index=False)  # save csv file
            is_added = True if len(df_result) > len(df_base) else False

        return wine, df_result.to_dict('records'), is_added


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
        self.dataset_manager = DatasetManager()
        self.metrics_path = f"./app/datasource/predictors/{metrics_filename}"
        self.added_data_path = None
        for path in [self.model_path, self.metrics_path]:
            if not os.path.exists(path):
                raise ValueError(f"Path '{path}' not exists... Please check the path")

        self.model = None
        self.metrics = None
        self.parameters = None

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

    def __preprocessing(self, df_wines: pd.DataFrame) -> pd.DataFrame:
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

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        return X_train, X_test, y_train, y_test

    def train(self):

        df_wines = self.dataset_manager.get_dataset()
        X_train, X_test, y_train, y_test = self.__preprocessing(df_wines)
        # todo : train the model
        if self.model:
            return True
            self.model.fit(df_wines_preprocessing)
            self.metrics = self.model.score(df_wines_preprocessing)
            self.save_model(self.model_path, self.metrics_path)
