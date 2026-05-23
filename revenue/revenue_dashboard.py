import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

def analyze_growth(file):

    if file.name.endswith(".csv"):
        df=pd.read_csv(file.name)

    elif file.name.endswith(".xlsx"):
        df=pd.read_excel(file.name)

    else:
        return None,None,None,None,None

    df_2024=df[
        df["Year"]==2024
    ]

    df_2025=df[
        df["Year"]==2025
    ]

    revenue_2024=df_2024[
        "Total_Fee_Collection"
    ].mean()

    revenue_2025=df_2025[
        "Total_Fee_Collection"
    ].mean()

    admission_2024=df_2024[
        "New_Admissions"
    ].mean()

    admission_2025=df_2025[
        "New_Admissions"
    ].mean()

    retention_2024=df_2024[
        "Retention_Rate"
    ].mean()

    retention_2025=df_2025[
        "Retention_Rate"
    ].mean()

    revenue_growth=(
        (
            revenue_2025-
            revenue_2024
        )/revenue_2024
    )*100

    admission_growth=(
        (
            admission_2025-
            admission_2024
        )/admission_2024
    )*100

    retention_growth=(
        (
            retention_2025-
            retention_2024
        )/retention_2024
    )*100

    summary=f"""
Revenue 2024 : ₹{int(revenue_2024)}

Revenue 2025 : ₹{int(revenue_2025)}

Revenue Growth : {revenue_growth:.2f}%

Admissions Growth : {admission_growth:.2f}%

Retention Improvement : {retention_growth:.2f}%
"""

    plt.figure(figsize=(7,5))

    years=[
        "2024",
        "2025"
    ]

    revenues=[
        revenue_2024,
        revenue_2025
    ]

    plt.bar(
        years,
        revenues
    )

    plt.title(
        "Revenue Comparison"
    )

    plt.ylabel(
        "Revenue"
    )

    revenue_chart="revenue_chart.png"

    plt.savefig(
        revenue_chart,
        bbox_inches='tight'
    )

    plt.close()

    plt.figure(figsize=(7,5))

    admissions=[
        admission_2024,
        admission_2025
    ]

    plt.plot(
        years,
        admissions,
        marker='o'
    )

    plt.title(
        "Admissions Growth"
    )

    plt.ylabel(
        "Admissions"
    )

    admission_chart="admission_chart.png"

    plt.savefig(
        admission_chart,
        bbox_inches='tight'
    )

    plt.close()

    infra_2024=(
        df_2024[
            "Smart_Classrooms"
        ].mean()+
        df_2024[
            "Lab_Facilities"
        ].mean()+
        df_2024[
            "Digital_Learning_Support"
        ].mean()
    )/3

    infra_2025=(
        df_2025[
            "Smart_Classrooms"
        ].mean()+
        df_2025[
            "Lab_Facilities"
        ].mean()+
        df_2025[
            "Digital_Learning_Support"
        ].mean()
    )/3

    insights=f"""
Why Revenue Increased:

- Better infrastructure development
- Improved digital learning
- Increased admissions
- Better academic performance
- Improved retention rates

Infrastructure Growth:
{((infra_2025-infra_2024)/infra_2024)*100:.2f}%

Suggested Improvements:
- Expand smart classrooms
- Increase innovation programs
- Improve sports facilities
- Increase AI workshops
"""

    comparison_df=pd.DataFrame({

        "Metric":[
            "Revenue",
            "Admissions",
            "Retention"
        ],

        "2024":[
            int(revenue_2024),
            int(admission_2024),
            round(retention_2024,2)
        ],

        "2025":[
            int(revenue_2025),
            int(admission_2025),
            round(retention_2025,2)
        ]
    })

    return (
        comparison_df,
        summary,
        revenue_chart,
        admission_chart,
        insights
    )

with gr.Blocks(
    title="AI School Growth Analytics"
) as app:

    gr.Markdown("""
# 🏫 AI School Growth Analytics Platform

Upload merged dataset and AI will:
- Compare 2024 vs 2025
- Analyze revenue growth
- Analyze admissions growth
- Detect growth factors
- Suggest strategies
""")

    with gr.Row(equal_height=True):

        with gr.Column(scale=1):

            file_input=gr.File(
                label="Upload Growth Dataset"
            )

            analyze_btn=gr.Button(
                "🚀 Analyze Growth",
                variant="primary",
                size="lg"
            )

            summary_box=gr.Textbox(
                label="📊 Growth Summary",
                lines=10
            )

            insights_box=gr.Textbox(
                label="🧠 AI Growth Insights",
                lines=14
            )

        with gr.Column(scale=2):

            result_table=gr.Dataframe(
                label="📈 Year Comparison"
            )

            with gr.Row():

                revenue_output=gr.Image(
                    label="💰 Revenue Comparison"
                )

                admission_output=gr.Image(
                    label="🎓 Admissions Growth"
                )

    analyze_btn.click(
        fn=analyze_growth,
        inputs=file_input,
        outputs=[
            result_table,
            summary_box,
            revenue_output,
            admission_output,
            insights_box
        ]
    )

app.launch(
    server_port=1000
)