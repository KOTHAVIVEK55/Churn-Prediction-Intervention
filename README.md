# AI School Growth Analytics & Churn Prediction Platform

![AI School Growth Analytics](./school_preview.png)

An AI-powered enterprise-grade predictive analytics platform designed to help school administrators improve student retention, forecast future revenues, and identify critical student churn factors using Machine Learning models.

---

## 🚀 Key Modules & Architecture

### 1. User Authentication & Gateway Backend (`/backend`)
A secure user portal and gateway system that authenticates administrators and orchestrates notifications.
- **Tech Stack**: Node.js, Express.js, RESTful APIs, dotenv
- **Core Components**:
  - `server.js`: Entrypoint for the backend server
  - `routes/authRoutes.js`: Admin registration and login handling
  - `routes/whatsappRoutes.js`: Notification trigger hooks (supporting future WhatsApp/SMS alerting)
  - `public/`: Gateway frontend landing portal styled with custom CSS (`style.css`, `script.js`)

### 2. Student Churn Prediction Engine (`/pro`)
Predicts the probability of a student dropping out using Machine Learning models trained on historical student enrollment datasets.
- **Tech Stack**: Python, Pandas, NumPy, Scikit-learn, XGBoost
- **Core Components**:
  - `train_model.py`: Model training script which analyzes 5,000+ student records
  - `dataset.py`: Data ingestion and cleaning pipeline
  - `risk_distribution.png` & `top_churn_reasons.png`: Visual representations of churn risk factors
  - `churn_model.pkl`: Serialized machine learning model ready for inference

### 3. Revenue Forecasting Engine (`/revenue`)
Models future student enrollment intakes and predicts institution revenue dynamics.
- **Tech Stack**: Python, Pandas, Matplotlib, Scikit-learn
- **Core Components**:
  - `revenue_dashboard.py`: Interactive python dashboard showcasing admission and income forecasts
  - `merge_dataset.py`: Consolidates multi-year spreadsheet records (`school_income_dataset_2024.xlsx`, `2025.xlsx`)
  - `admission_chart.png` & `revenue_chart.png`: Graphic forecasting charts
  - `revenue_prediction/`: Core predictive modeling scripts (`model.py`, `dashboard.py`, `growth_model.pkl`)

### 4. Application Orchestrator (`Root`)
- `main_app.py`: Integrated central UI dashboard orchestrating the predictive modules.
- `launcher.py`: Utility startup orchestrator for launching the platform components simultaneously.

---

## 📂 Project Directory Structure

```directory
school_project/
├── backend/                       # Gateway authentication backend (Node/Express)
│   ├── routes/                    # API route files (auth, notifications)
│   ├── public/                    # Admin portal login/register frontend
│   └── server.js                  # Backend express application
├── pro/                           # Churn Prediction machine learning module
│   ├── train_model.py             # Script to fit model and produce plots
│   └── dataset.py                 # Feature engineering pipeline
├── revenue/                       # Revenue Prediction module
│   ├── revenue_prediction/        # Under-the-hood prediction algorithms and models
│   ├── revenue_dashboard.py       # GUI dashboard showing revenue projections
│   └── merge_dataset.py           # Multi-year intake consolidation
├── launcher.py                    # Root shell orchestrator
├── main_app.py                    # Integrated central user dashboard
├── requirements.txt               # Required Python packages
└── README.md                      # Documentation & guides
```

---

## 🔧 Installation & Setup

### 1. Clone & Set Up the Repository
```bash
git clone https://github.com/KOTHAVIVEK55/Churn-Prediction-Interention.git
cd Churn-Prediction-Interention
```

### 2. Set Up the Authentication Backend
Navigate to the `/backend` folder, install Node packages, and run the Express gateway:
```bash
cd backend
npm install
node server.js
```
The authentication server will start running locally.

### 3. Set Up Python Environment & Run Dashboard
Install the required machine learning dependencies and run the central dashboard:
```bash
cd ..
pip install -r requirements.txt
python main_app.py
```
Open the generated local Gradio/Streamlit URL in your browser to interact with the growth charts and churn models.
