import gradio as gr
import pandas as pd
import joblib
import matplotlib.pyplot as plt

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model=joblib.load(os.path.join(BASE_DIR, "churn_model.pkl"))

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
        
    for col in ["Parent_Contact", "Phone_Number", "Contact", "Phone", "Mobile"]:
        if col in df.columns:
            drop_cols.append(col)

    X=df.drop(
        drop_cols,
        axis=1
    )

    probabilities=model.predict_proba(X)[:,1]

    original_df["Risk_Percentage"]=(
        probabilities*100
    ).round(2)

    risk_category=[]
    reasons_list=[]
    recommendations_list=[]

    safe_count=0
    moderate_count=0
    high_count=0

    reason_counter={
        "Low Attendance":0,
        "Poor Academics":0,
        "Fee Delay":0,
        "Discipline Issues":0,
        "Low Participation":0,
        "Low Satisfaction":0,
        "Travel Distance":0
    }

    for i in range(len(original_df)):

        row=original_df.iloc[i]

        risk=original_df.iloc[i][
            "Risk_Percentage"
        ]

        reasons=[]
        recommendations=[]

        score=0

        if row["Attendance"]<60:
            score+=2
            reasons.append(
                "Low Attendance"
            )
            recommendations.append(
                "Parent Counseling"
            )
            reason_counter[
                "Low Attendance"
            ]+=1

        if row["Marks"]<50:
            score+=2
            reasons.append(
                "Poor Academic Performance"
            )
            recommendations.append(
                "Academic Mentoring"
            )
            reason_counter[
                "Poor Academics"
            ]+=1

        if row["Fee_Delay"]=="Yes":
            score+=2
            reasons.append(
                "Fee Payment Delay"
            )
            recommendations.append(
                "Flexible Fee Support"
            )
            reason_counter[
                "Fee Delay"
            ]+=1

        if row["Discipline_Issues"]>=3:
            score+=1
            reasons.append(
                "Discipline Issues"
            )
            recommendations.append(
                "Behavioral Counseling"
            )
            reason_counter[
                "Discipline Issues"
            ]+=1

        if row["Participation_Level"]=="Low":
            score+=1
            reasons.append(
                "Low Participation"
            )
            recommendations.append(
                "Extracurricular Engagement"
            )
            reason_counter[
                "Low Participation"
            ]+=1

        if row["Satisfaction_Score"]<4:
            score+=2
            reasons.append(
                "Low Satisfaction"
            )
            recommendations.append(
                "Student Wellness Programs"
            )
            reason_counter[
                "Low Satisfaction"
            ]+=1

        if row["Distance_From_School_KM"]>15:
            score+=1
            reasons.append(
                "Long Travel Distance"
            )
            recommendations.append(
                "Transport Assistance"
            )
            reason_counter[
                "Travel Distance"
            ]+=1

        if len(recommendations)==0:
            recommendations.append(
                "No Immediate Intervention Needed"
            )

        if len(reasons)==0:
            reasons.append(
                "No Major Risk Factors"
            )

        if risk<30 and score<=2:
            category="SAFE"
            safe_count+=1

        elif risk<60 or score<=5:
            category="MODERATE RISK"
            moderate_count+=1

        else:
            category="HIGH RISK"
            high_count+=1

        risk_category.append(category)

        reasons_list.append(
            ", ".join(reasons)
        )

        recommendations_list.append(
            ", ".join(recommendations)
        )

    original_df["Risk_Category"]=risk_category
    original_df["Risk_Reasons"]=reasons_list
    original_df["Recommendations"]=recommendations_list

    output_file="student_churn_analysis.xlsx"

    original_df.to_excel(
        output_file,
        index=False
    )

    preview_df=original_df[[
        "Student_ID",
        "Attendance",
        "Marks",
        "Risk_Percentage",
        "Risk_Category",
        "Risk_Reasons",
        "Recommendations"
    ]]

    total_students=len(original_df)

    summary=f"""
Total Students : {total_students}

SAFE Students : {safe_count}

MODERATE RISK Students : {moderate_count}

HIGH RISK Students : {high_count}
"""

    plt.figure(figsize=(5,5))

    risk_data=[
        safe_count,
        moderate_count,
        high_count
    ]

    risk_labels=[
        "SAFE",
        "MODERATE",
        "HIGH RISK"
    ]

    plt.pie(
        risk_data,
        labels=risk_labels,
        autopct='%1.1f%%'
    )

    plt.title(
        "Student Risk Distribution"
    )

    pie_chart="risk_distribution.png"

    plt.savefig(
        pie_chart,
        bbox_inches='tight'
    )

    plt.close()

    plt.figure(figsize=(7,5))

    plt.bar(
        reason_counter.keys(),
        reason_counter.values()
    )

    plt.xticks(rotation=10)

    plt.title(
        "Top Student Churn Reasons"
    )

    plt.xlabel("Reasons")

    plt.ylabel("Count")

    bar_chart="top_churn_reasons.png"

    plt.savefig(
        bar_chart,
        bbox_inches='tight'
    )

    plt.close()

    top_reason=max(
        reason_counter,
        key=reason_counter.get
    )

    insights=f"""
Most students are at risk due to:

{top_reason}

Suggested School Actions:
- Improve attendance monitoring
- Increase parent engagement
- Provide student support programs
"""

    return (
        preview_df,
        output_file,
        summary,
        pie_chart,
        bar_chart,
        insights
    )

import requests

def send_alerts(file):
    if not file:
        return "⚠️ Please upload and analyze a dataset first."
    
    try:
        # Read the analysis output
        df = pd.read_excel("student_churn_analysis.xlsx")
    except:
        return "⚠️ Could not find analysis results. Click 'Analyze Dataset' first."
        
    if "Risk_Category" not in df.columns:
        return "⚠️ Dataset not analyzed. Click 'Analyze Dataset' first."
        
    # Check for phone column (accept common variations)
    phone_col = None
    for col in ["Parent_Contact", "Phone_Number", "Contact", "Phone", "Mobile"]:
        if col in df.columns:
            phone_col = col
            break
            
    if not phone_col:
        return "❌ Error: Could not find a phone number column (looked for Parent_Contact, Phone, Mobile, etc.) in your dataset."
        
    # Filter high risk
    high_risk_df = df[df["Risk_Category"] == "HIGH RISK"]
    
    if len(high_risk_df) == 0:
        return "✅ No HIGH RISK students found. No alerts needed."
        
    success_count = 0
    fail_count = 0
    
    for _, row in high_risk_df.iterrows():
        phone_raw = str(row[phone_col]).strip()
        if phone_raw.endswith('.0'):
            phone_raw = phone_raw[:-2]
            
        # Extract only digits
        phone_digits = ''.join(filter(str.isdigit, phone_raw))
        
        if not phone_digits or phone_raw == 'nan':
            fail_count += 1
            continue
            
        # Twilio requires E.164 format. If it's 10 digits, assume India (+91)
        if len(phone_digits) == 10:
            phone = "+91" + phone_digits
        else:
            phone = "+" + phone_digits
            
        payload = {
            "studentPhone": phone,
            "riskCategory": row["Risk_Category"],
            "riskPercentage": row["Risk_Percentage"],
            "insights": row["Recommendations"]
        }
        
        try:
            res = requests.post("http://localhost:3000/api/whatsapp/send", json=payload, timeout=5)
            if res.status_code == 200:
                success_count += 1
            else:
                fail_count += 1
        except:
            fail_count += 1
            
    return f"📱 Bulk WhatsApp Dispatch Complete:\n✅ Successfully Sent: {success_count}\n❌ Failed/Skipped: {fail_count}"

with gr.Blocks(
    title="AI School Churn Analytics"
) as app:

    gr.Markdown("""
# 🎓 AI School Churn Analytics System

Upload dataset and AI will:
- Predict churn risk
- Detect reasons
- Suggest interventions
- Generate analytics dashboard
""")

    with gr.Row(equal_height=True):

        with gr.Column(scale=1):

            gr.Markdown("## 📂 Upload & Controls")

            file_input=gr.File(
                label="Upload Student Dataset"
            )

            analyze_btn=gr.Button(
                "Analyze Dataset",
                variant="primary",
                size="lg"
            )
            
            send_alerts_btn = gr.Button(
                "📲 Auto-Send WhatsApp Alerts (High Risk)",
                variant="secondary"
            )
            
            alert_status = gr.Textbox(
                label="WhatsApp Dispatch Status",
                interactive=False
            )

            summary_box=gr.Textbox(
                label="📊 Analysis Summary",
                lines=8
                
            )

            insight_box=gr.Textbox(
                label="🧠 AI Insights",
                lines=8
            )

            download_output=gr.File(
                label="⬇️ Download Excel Report"
            )

        with gr.Column(scale=2):

            gr.Markdown("## 📈 Student Analytics Dashboard")

            result_table=gr.Dataframe(
                label="Student Risk Analysis",
                interactive=False,
                wrap=True
            )

            with gr.Row():

                pie_output=gr.Image(
                    label="📊 Risk Distribution"
                )

                bar_output=gr.Image(
                    label="📈 Top Churn Reasons"
                )

    analyze_btn.click(
        fn=analyze_dataset,
        inputs=file_input,
        outputs=[
            result_table,
            download_output,
            summary_box,
            pie_output,
            bar_output,
            insight_box
        ]
    )
    
    send_alerts_btn.click(
        fn=send_alerts,
        inputs=file_input,
        outputs=alert_status
    )

app.launch(server_port=7860, root_path="/churn")
