import gradio as gr
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os

BASE_DIR=os.path.dirname(__file__)

model=joblib.load(
    os.path.join(BASE_DIR,"churn_model.pkl")
)

def analyze_dataset(file):

    if file.name.endswith(".csv"):
        df=pd.read_csv(file.name)

    elif file.name.endswith(".xlsx"):
        df=pd.read_excel(file.name)

    else:
        return None,None,None,None,None,None

    original_df=df.copy()

    df["Fee_Delay"]=df["Fee_Delay"].map({
        "No":0,
        "Yes":1
    })

    participation_map={
        "Low":0,
        "Medium":1,
        "High":2
    }

    df["Participation_Level"]=df["Participation_Level"].map(
        participation_map
    )

    feedback_map={
        "Poor":0,
        "Average":1,
        "Good":2
    }

    df["Parent_Feedback"]=df["Parent_Feedback"].map(
        feedback_map
    )

    binary_cols=[
        "Extra_Classes_Attended",
        "Scholarship_Status",
        "Sports_Programs",
        "Cultural_Events",
        "Innovation_Programs",
        "Olympiad_Support",
        "Career_Guidance",
        "Personality_Development",
        "AI_Tech_Workshops"
    ]

    for col in binary_cols:

        yes_no_map={
            "No":0,
            "Yes":1
        }

        if df[col].dtype=="object":
            df[col]=df[col].map(
                yes_no_map
            )

    drop_cols=["Student_ID"]

    if "Churn" in df.columns:
        drop_cols.append("Churn")

    X=df.drop(
        drop_cols,
        axis=1
    )

    probabilities=model.predict_proba(X)[:,1]

    original_df["Risk_Percentage"]=(
        probabilities*100
    ).round(2)

    risk_category=[]

    safe_count=0
    moderate_count=0
    high_count=0

    for i in range(len(original_df)):

        risk=original_df.iloc[i]["Risk_Percentage"]

        if risk<30:
            category="SAFE"
            safe_count+=1

        elif risk<60:
            category="MODERATE RISK"
            moderate_count+=1

        else:
            category="HIGH RISK"
            high_count+=1

        risk_category.append(category)

    original_df["Risk_Category"]=risk_category

    output_file="student_churn_analysis.xlsx"

    original_df.to_excel(
        output_file,
        index=False
    )

    preview_df=original_df.head(20)

    summary=f"""
SAFE Students : {safe_count}

MODERATE Students : {moderate_count}

HIGH RISK Students : {high_count}
"""

    plt.figure(figsize=(5,5))

    plt.pie(
        [safe_count,moderate_count,high_count],
        labels=["SAFE","MODERATE","HIGH"],
        autopct='%1.1f%%'
    )

    pie_chart="risk_distribution.png"

    plt.savefig(pie_chart)

    plt.close()

    insights="""
AI Suggestions:
- Improve attendance
- Parent counseling
- Student engagement
"""

    return (
        preview_df,
        output_file,
        summary,
        pie_chart,
        insights
    )

def create_churn_tab():

    with gr.Blocks() as app:

        gr.Markdown(
            "# 📉 AI Student Churn Prediction"
        )

        with gr.Row():

            with gr.Column():

                file_input=gr.File()

                analyze_btn=gr.Button(
                    "Analyze"
                )

                summary_box=gr.Textbox(
                    label="Summary"
                )

                insight_box=gr.Textbox(
                    label="AI Insights"
                )

                download_output=gr.File()

            with gr.Column():

                result_table=gr.Dataframe()

                pie_output=gr.Image()

        analyze_btn.click(
            fn=analyze_dataset,
            inputs=file_input,
            outputs=[
                result_table,
                download_output,
                summary_box,
                pie_output,
                insight_box
            ]
        )

    return app