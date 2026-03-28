from lazypredict.Supervised import LazyRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

data = pd.read_csv(r"C:\Users\Shreyash\tripduration\tripduration\data\processed\train.csv")
X = data.drop('trip_duration', axis=1)
y = data['trip_duration']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
clf = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
models, predictions = clf.fit(X_train, X_test, y_train, y_test)
print(models)