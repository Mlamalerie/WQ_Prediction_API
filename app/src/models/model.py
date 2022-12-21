class Model():
    name: str
    model : RandomForestClassifier
    model_path : str
    data_path : str
    metrics: dict
    metrics_path : str
    parameters : dict

    def __init__(self, name, version, model_path, data_path, metrics_path):
        self.name = name
        self.model_path = model_path
        self.data_path = data_path
        self.metrics_path = metrics_path
        self.metrics = None
        self.parameters = None
        self.load_model(model_path)
        self.get_metrics()
        self.get_parameters()

