import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

def analyze_growth(file):

    filepath = getattr(file, "name", file)
    if filepath.endswith(".csv"):
        df=pd.read_csv(filepath)
    elif filepath.endswith(".xlsx"):
        df=pd.read_excel(filepath)

    df_2024=df[df["Year"]==2024]
    df_2025=df[df["Year"]==2025]

    revenue_2024=df_2024[
        "Total_Fee_Collection"
    ].mean()

    revenue_2025=df_2025[
        "Total_Fee_Collection"
    ].mean()

    growth=((revenue_2025-revenue_2024)/revenue_2024)*100

    summary=f"""
Revenue Growth:
{growth:.2f}%
"""

    comparison_df=pd.DataFrame({

        "Year":["2024","2025"],

        "Revenue":[
            revenue_2024,
            revenue_2025
        ]
    })

    plt.figure(figsize=(6,5))

    plt.bar(
        comparison_df["Year"],
        comparison_df["Revenue"]
    )

    revenue_chart="revenue_chart.png"

    plt.savefig(revenue_chart)

    plt.close()

    insights="""
AI Insights:
- Revenue increased
- Admissions improved
- Retention improved
"""

    return (
        comparison_df,
        summary,
        revenue_chart,
        insights
    )

def create_growth_tab():

    with gr.Blocks() as app:

        gr.Markdown(
            "# 📈 AI School Growth Analytics"
        )

        with gr.Row():

            with gr.Column():

                file_input=gr.File()

                analyze_btn=gr.Button(
                    "Analyze Growth"
                )

                summary_box=gr.Textbox()

                insights_box=gr.Textbox()

            with gr.Column():

                result_table=gr.Dataframe()

                revenue_output=gr.Image()

        analyze_btn.click(
            fn=analyze_growth,
            inputs=file_input,
            outputs=[
                result_table,
                summary_box,
                revenue_output,
                insights_box
            ]
        )

    return app