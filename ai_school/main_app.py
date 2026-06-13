import gradio as gr

from churn.app import create_churn_tab
from growth.revenue_dashboard import create_growth_tab
from future.dashboard import create_future_tab

with gr.Blocks(
    title="AI School Analytics Platform",
    theme=gr.themes.Soft()
) as demo:
    gr.Markdown("""

# 🎓 AI SCHOOL ANALYTICS PLATFORM

Complete AI ecosystem for:

- Student Churn Prediction
- School Growth Analytics
- Future Forecasting

""")

    with gr.Tabs():
        with gr.Tab("📉 Churn Prediction"):
            create_churn_tab()

        with gr.Tab("📈 Growth Analytics"):
            create_growth_tab()

        with gr.Tab("🚀 Future Prediction"):
            create_future_tab()

demo.launch(server_port=7860)