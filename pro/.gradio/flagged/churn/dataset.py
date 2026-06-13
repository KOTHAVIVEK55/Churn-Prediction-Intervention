


import pandas as pd
import numpy as np
import random
random.seed(42)
np.random.seed(42)
n=5000
student_data=[]
for i in range(n):
    attendance=random.randint(40,100)
    marks=random.randint(35,100)
    fee_delay=random.choice(["Yes","No"])
    discipline=random.randint(0,5)
    participation=random.choice(["Low","Medium","High"])
    satisfaction=random.randint(1,10)
    distance=random.randint(1,25)
    parent_feedback=random.choice(["Poor","Average","Good"])
    extra_classes=random.choice(["Yes","No"])
    scholarship=random.choice(["Yes","No"])
    sports=random.choice(["Yes","No"])
    cultural=random.choice(["Yes","No"])
    innovation=random.choice(["Yes","No"])
    olympiad=random.choice(["Yes","No"])
    career=random.choice(["Yes","No"])
    personality=random.choice(["Yes","No"])
    ai_workshop=random.choice(["Yes","No"])
    churn_probability=0
    if attendance<60:
        churn_probability+=30
    if marks<45:
        churn_probability+=25
    if satisfaction<4:
        churn_probability+=20
    if fee_delay=="Yes":
        churn_probability+=15
    if participation=="Low":
        churn_probability+=10
    random_factor=random.randint(0,30)
    churn_probability+=random_factor
    if churn_probability>=50:
        churn="Yes"
    else:
        churn="No"
    student_data.append({
        "Student_ID":i+1,
        "Attendance":attendance,
        "Marks":marks,
        "Fee_Delay":fee_delay,
        "Discipline_Issues":discipline,
        "Participation_Level":participation,
        "Satisfaction_Score":satisfaction,
        "Distance_From_School_KM":distance,
        "Parent_Feedback":parent_feedback,
        "Extra_Classes_Attended":extra_classes,
        "Scholarship_Status":scholarship,
        "Sports_Programs":sports,
        "Cultural_Events":cultural,
        "Innovation_Programs":innovation,
        "Olympiad_Support":olympiad,
        "Career_Guidance":career,
        "Personality_Development":personality,
        "AI_Tech_Workshops":ai_workshop,
        "Churn":churn
    })

student_df=pd.DataFrame(student_data)

student_df.to_csv("student_dataset_5000.csv",index=False)

print("Dataset Generated")