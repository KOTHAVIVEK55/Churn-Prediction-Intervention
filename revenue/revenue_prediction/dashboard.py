import gradio as gr
import pandas as pd
import joblib

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model=joblib.load(os.path.join(BASE_DIR, "growth_model.pkl"))

def predict_growth(file):

    if file.name.endswith(".csv"):
        df=pd.read_csv(file.name)

    elif file.name.endswith(".xlsx"):
        df=pd.read_excel(file.name)

    else:
        return None,None,None,None,None

    X=df.drop(
        ["Future_Growth_Trend"],
        axis=1,
        errors="ignore"
    )

    prediction=model.predict(X)[0]

    growth_map={
        0:"High Growth",
        1:"Low Growth",
        2:"Moderate Growth"
    }

    result=growth_map[
        prediction
    ]

    row=df.iloc[0]

    current_score=(
        row["Infrastructure_Development"]+
        row["Teaching_Quality_Improvement"]+
        row["Digital_Learning_Adoption"]+
        row["Student_Satisfaction"]+
        row["New_Programs_Introduced"]+
        row["Marketing_Reach"]
    )

    if result=="High Growth":
        future_score=current_score+10

    elif result=="Moderate Growth":
        future_score=current_score+5

    else:
        future_score=current_score-5

    suggestions=[]

    if row["Infrastructure_Development"]<8:
        suggestions.append(
            "Improve Infrastructure Development"
        )

    if row["Teaching_Quality_Improvement"]<8:
        suggestions.append(
            "Improve Teaching Quality"
        )

    if row["Digital_Learning_Adoption"]<8:
        suggestions.append(
            "Expand Digital Learning"
        )

    if row["Student_Satisfaction"]<8:
        suggestions.append(
            "Improve Student Satisfaction"
        )

    if row["New_Programs_Introduced"]<8:
        suggestions.append(
            "Introduce More Innovation Programs"
        )

    if row["Marketing_Reach"]<8:
        suggestions.append(
            "Increase Marketing Reach"
        )

    if row["Retention_Rate"]<85:
        suggestions.append(
            "Improve Retention Rate"
        )

    if len(suggestions)==0:

        recommendation_text="""
School performance is excellent.

Future Strategies:
- Continue innovation programs
- Maintain teaching quality
- Expand AI learning initiatives
- Improve national visibility
"""

    else:

        recommendation_text="\n".join(
            suggestions
        )

    current_text=f"""
Current School Status (2025)

Growth Prediction:
{result}

Current Performance Score:
{current_score}

Predicted 2026 Score:
{future_score}
"""

    chart_data=pd.DataFrame({

        "Year":[
            "2024",
            "2025",
            "2026"
        ],

        "Growth":[
            current_score-8,
            current_score,
            future_score
        ],

        "Type":[
            "Past",
            "Current",
            "Predicted"
        ]
    })

    return (
        current_text,
        recommendation_text,
        chart_data,
        chart_data,
        result
    )

with gr.Blocks(
    title="AI School Growth Predictor"
) as app:

    gr.Markdown("""
# 🚀 AI School Future Growth Prediction System
""")

    with gr.Row():

        with gr.Column(scale=1):

            file_input=gr.File(
                label="Upload School Dataset"
            )

            predict_btn=gr.Button(
                "🚀 Predict 2026 Growth",
                variant="primary",
                size="lg"
            )

            growth_label=gr.Label(
                label="2026 Growth Prediction"
            )

            current_box=gr.Textbox(
                label="📊 Current School Status",
                lines=10
            )

            recommendation_output=gr.Textbox(
                label="🧠 AI Suggestions",
                lines=12
            )

        with gr.Column(scale=1):

            chart_output=gr.BarPlot(
                x="Year",
                y="Growth",
                color="Type",
                title="2025 vs 2026 Growth Analysis"
            )

            line_chart=gr.LinePlot(
                x="Year",
                y="Growth",
                title="2024 → 2025 → 2026 Growth Trend"
            )

    predict_btn.click(
        fn=predict_growth,
        inputs=file_input,
        outputs=[
            current_box,
            recommendation_output,
            chart_output,
            line_chart,
            growth_label
        ]
    )

app.launch(
    server_port=1002,
    root_path="/future",
    theme=gr.themes.Soft(
        primary_hue="orange"
    )
)