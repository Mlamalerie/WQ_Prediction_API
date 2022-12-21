# Wine Quality Predictor 🍷

## 📦 Dataset
1153 samples wine with 12 features each. 

The features are:
- fixed acidity
- volatile acidity
- citric acid
- residual sugar
- chlorides
- free sulfur dioxide
- total sulfur dioxide
- density
- pH
- sulphates
- alcohol
- **quality** (score between 0 and 10)

## ⚙️ How to use it
- Clone the repository
- Create a virtual environment with the following command:
```
virtualenv -p python3 venv
```
- Activate the virtual environment with the following command:
```
source venv/bin/activate
```
- Install the requirements with the following command:
```
pip install -r requirements.txt
```

- Go to the app folder with the following command:
```
cd app
```
- Run the app with the following command:
```
uvicorn main:app --reload
```
- The app default to the following url:
```
127.0.0.1:8000
```
- You can access the documentation of the API at the followings url:
```
127.0.0.1:800/docs
127.0.0.1:800/redoc
```