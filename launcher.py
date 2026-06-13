import gradio as gr

custom_css = """
body{
    background-color:#0b1020;
}

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    margin-top:20px;
    color:white;
}

.sub-title{
    text-align:center;
    font-size:18px;
    color:#cbd5e1;
    margin-bottom:40px;
}

.card{
    background:linear-gradient(145deg,#111827,#1f2937);
    padding:30px;
    border-radius:20px;
    text-align:center;
    transition:0.3s;
    border:1px solid #374151;
    box-shadow:0px 0px 20px rgba(0,0,0,0.3);
}

.card:hover{
    transform:scale(1.03);
    border:1px solid #6366f1;
    box-shadow:0px 0px 30px rgba(99,102,241,0.5);
}

.card-title{
    font-size:26px;
    font-weight:bold;
    margin-top:15px;
    color:white;
}

.card-desc{
    color:#cbd5e1;
    margin-top:10px;
    margin-bottom:20px;
    font-size:16px;
}

.open-btn{
    display:inline-block;
    background:#6366f1;
    color:white !important;
    padding:12px 22px;
    border-radius:12px;
    text-decoration:none;
    font-weight:bold;
    transition:0.3s;
}

.open-btn:hover{
    background:#818cf8;
}

.footer{
    text-align:center;
    margin-top:40px;
    color:#94a3b8;
}
"""

with gr.Blocks(
    title="AI School Analytics Platform",
    css=custom_css
) as app:

    gr.HTML("""
    <div class="main-title">
        🎓 AI SCHOOL ANALYTICS PLATFORM
    </div>

    <div class="sub-title">
        Unified AI ecosystem for intelligent educational analytics
    </div>
    """)

    with gr.Row():

        with gr.Column():

            gr.HTML("""

            <div class="card">

                <div style="font-size:60px;">
                    📉
                </div>

                <div class="card-title">
                    Student Churn Prediction
                </div>

                <div class="card-desc">
                    Predict at-risk students using AI-powered analytics,
                    risk detection, intervention planning, and churn insights.
                </div>

                <a class="open-btn"
                   href="http://127.0.0.1:7860"
                   target="_blank">

                   Open System

                </a>

            </div>

            """)

        with gr.Column():

            gr.HTML("""

            <div class="card">

                <div style="font-size:60px;">
                    📈
                </div>

                <div class="card-title">
                    School Growth Analytics
                </div>

                <div class="card-desc">
                    Analyze revenue growth, admissions trends,
                    retention performance, and institutional growth factors.
                </div>

                <a class="open-btn"
                   href="http://127.0.0.1:1000"
                   target="_blank">

                   Open System

                </a>

            </div>

            """)

        with gr.Column():

            gr.HTML("""

            <div class="card">

                <div style="font-size:60px;">
                    🚀
                </div>

                <div class="card-title">
                    Future Growth Prediction
                </div>

                <div class="card-desc">
                    Forecast future school performance using
                    AI-based predictive growth intelligence.
                </div>

                <a class="open-btn"
                   href="http://127.0.0.1:1002"
                   target="_blank">

                   Open System

                </a>

            </div>

            """)

    gr.HTML("""

    <div class="footer">
        Built with Gradio • Machine Learning • XGBoost • Random Forest
    </div>

    """)

app.launch(server_port=2000)