import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report
import joblib

student_df=pd.read_csv("student_dataset_5000.csv")

le=LabelEncoder()

categorical_cols=[
"Fee_Delay",
"Participation_Level",
"Parent_Feedback",
"Extra_Classes_Attended",
"Scholarship_Status",
"Sports_Programs",
"Cultural_Events",
"Innovation_Programs",
"Olympiad_Support",
"Career_Guidance",
"Personality_Development",
"AI_Tech_Workshops",
"Churn"
]

for col in categorical_cols:
    student_df[col]=le.fit_transform(student_df[col])

X=student_df.drop(
["Student_ID","Churn"],
axis=1
)

y=student_df["Churn"]

X_train,X_test,y_train,y_test=train_test_split(
X,
y,
test_size=0.3,
random_state=42
)

model=RandomForestClassifier(
n_estimators=100,
max_depth=5,
random_state=42
)

model.fit(X_train,y_train)

y_pred=model.predict(X_test)

accuracy=accuracy_score(
y_test,
y_pred
)

print("\nAccuracy:\n")
print(accuracy)

print("\nClassification Report:\n")

print(
classification_report(
y_test,
y_pred
)
)

joblib.dump(
model,
"churn_model.pkl"
)

print("\nModel Saved Successfully")