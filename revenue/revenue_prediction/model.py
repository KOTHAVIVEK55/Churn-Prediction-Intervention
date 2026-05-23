import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import joblib

df=pd.read_excel(
    "growth_dataset.xlsx"
)

le=LabelEncoder()

df["Future_Growth_Trend"]=le.fit_transform(
    df["Future_Growth_Trend"]
)

X=df.drop(
    ["Future_Growth_Trend"],
    axis=1
)

y=df["Future_Growth_Trend"]

X_train,X_test,y_train,y_test=train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model=XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

y_pred=model.predict(
    X_test
)

accuracy=accuracy_score(
    y_test,
    y_pred
)

print("\nAccuracy:\n")

print(accuracy)

joblib.dump(
    model,
    "growth_model.pkl"
)

print("\nModel Saved")