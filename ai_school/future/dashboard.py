import gradio as gr
import pandas as pd
import joblib
import os

BASE_DIR=os.path.dirname(__file__)

model=joblib.load(
    os.path.join(BASE_DIR,"growth_model.pkl")
)

def predict_growth(file):

    filepath = getattr(file, "name", file)
    if filepath.endswith(".csv"):
        df=pd.read_csv(filepath)
    elif filepath.endswith(".xlsx"):
        df=pd.read_excel(filepath)

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

    result=growth_map[prediction]

    return result

def create_future_tab():

    with gr.Blocks() as app:

        gr.Markdown(
            "# 🚀 AI Future Growth Prediction"
        )

        file_input=gr.File()

        predict_btn=gr.Button(
            "Predict Future"
        )

        result_box=gr.Textbox(
            label="Prediction"
        )

        predict_btn.click(
            fn=predict_growth,
            inputs=file_input,
            outputs=result_box
        )

    return app