# LedgerPilot AI — Autonomous Finance Controller

LedgerPilot AI is an AI-assisted finance operations platform designed to automate payment reconciliation and investigate financial exceptions.

The system combines a deterministic reconciliation engine for financial correctness with Google Gemini for exception investigation and natural-language finance assistance.

## 🚀 Key Features

- Payment, settlement, and bank transaction reconciliation
- Automatic detection of financial exceptions
- Missing settlement detection
- Missing bank transaction detection
- Fee mismatch detection
- Amount mismatch detection
- Delayed settlement detection
- Duplicate settlement detection
- Bank reference mismatch detection
- Partial reconciliation handling
- Gemini-powered exception investigation
- AI Finance Assistant for finance-related questions
- Ground-truth based evaluation
- Large-scale reconciliation benchmarking

## 🧠 Architecture

```text
                    LedgerPilot AI
                         |
          +--------------+--------------+
          |                             |
          v                             v
   Financial Records              Gemini AI
 Payment / Settlement /       Exception Investigation
 Bank Transactions             & Finance Assistant
          |
          v
+----------------------------+
| Deterministic              |
| Reconciliation Engine      |
+-------------+--------------+
              |
       +------+------+ 
       |             |
       v             v
    MATCHED     PARTIAL / EXCEPTION
                     |
                     v
              Gemini Investigation
                     |
                     v
             Explanation +
          Recommended Action
```

### Design Principle

Financial matching is handled using deterministic rules rather than asking an LLM to make mathematical reconciliation decisions.

Gemini is used where generative reasoning is useful:

- Explaining why an exception occurred
- Suggesting a recommended action
- Answering finance-operation questions

This separation improves reliability and makes the reconciliation results measurable.

## 🛠️ Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS
- JavaScript

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite

### AI

- Google Gemini
- `google-genai` SDK
- Gemini 2.5 Flash

## 📁 Project Structure

```text
ledgerpilot-ai/
│
├── backend/
│   ├── app/
│   │   ├── database/
│   │   ├── models/
│   │   └── services/
│   │       ├── data_generator.py
│   │       ├── reconciliation_engine.py
│   │       ├── gemini_service.py
│   │       ├── ai_agent.py
│   │       ├── finance_assistant.py
│   │       ├── evaluation.py
│   │       └── benchmark.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Varun-AI-Robotics/ledgerpilot-ai.git
cd ledgerpilot-ai
```

### 2. Backend setup

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Gemini

Create:

```text
backend/.env
```

Use:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Never commit your real `.env` file or API key to GitHub.

### 4. Start the backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## 📊 Reconciliation Scenarios

| Scenario | Description |
|---|---|
| MATCHED | Payment, settlement and bank transaction agree |
| FEE_MISMATCH | Settlement fee differs from expected fee |
| AMOUNT_MISMATCH | Settlement amount differs from expected amount |
| MISSING_SETTLEMENT | No settlement exists for a payment |
| MISSING_BANK_TRANSACTION | Settlement exists but bank transaction is missing |
| DELAYED_SETTLEMENT | Settlement occurs significantly later than expected |
| DUPLICATE_SETTLEMENT | Multiple settlement records exist for one payment |
| BANK_REFERENCE_MISMATCH | Bank reference does not match the payment |

## 📈 50K-Record Evaluation

The reconciliation engine was evaluated against **50,000 synthetic records**.

| Metric | Result |
|---|---:|
| Records | **50,000** |
| Correct status | **50,000** |
| Incorrect status | **0** |
| Accuracy | **100%** |
| Precision | **100%** |
| Recall | **100%** |
| F1 Score | **100%** |
| Exception detection rate | **100%** |
| Exception type accuracy | **100%** |
| False-match rate | **0%** |
| Processing time | **29.7983 seconds** |
| Throughput | **1,677.95 records/sec** |

### Exception Results

| Exception Type | Support | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Fee Mismatch | 2,015 | 100% | 100% | 100% |
| Amount Mismatch | 1,494 | 100% | 100% | 100% |
| Missing Settlement | 2,048 | 100% | 100% | 100% |
| Missing Bank Transaction | 1,395 | 100% | 100% | 100% |
| Delayed Settlement | 1,551 | 100% | 100% | 100% |
| Duplicate Settlement | 1,020 | 100% | 100% | 100% |
| Bank Reference Mismatch | 1,483 | 100% | 100% | 100% |

## 🔌 Main API Endpoints

```text
POST /api/generate-data
POST /api/reconcile
GET  /api/reconciliation
GET  /api/stats
GET  /api/metrics

GET  /api/ground-truth
GET  /api/ground-truth/stats

POST /api/ai/investigate
POST /api/ai/ask

POST /api/evaluation/run
GET  /api/evaluation/metrics
GET  /api/evaluation/history
POST /api/evaluation/benchmark
POST /api/evaluation/scale-benchmark
```

## 🔐 Security

- API keys are stored in environment variables.
- `.env` is excluded from Git using `.gitignore`.
- `.env.example` is provided for configuration reference.
- No production financial data is included in the repository.

## 🎯 Buildathon Goal

LedgerPilot AI closes a finance-operations loop:

```text
Financial Data
      ↓
Reconciliation
      ↓
Exception Detection
      ↓
AI Investigation
      ↓
Explanation
      ↓
Recommended Action
```

The goal is to reduce manual reconciliation effort while maintaining deterministic and measurable financial matching.

## ⚠️ Evaluation Note

The reported evaluation results are based on the project's synthetic ground-truth dataset. They should not be interpreted as production accuracy on real financial data.

Gemini is used for investigation and explanation; deterministic reconciliation rules are responsible for the financial matching decisions.

## 🖥️ Project Screenshots

| Backend — API & Reconciliation | Frontend — Finance Dashboard |
|:---:|:---:|
| <img src="[screenshots/backend-1.png](https://github.com/Varun-AI-Robotics/ledgerpilot-ai/blob/41beb77bd3acada2ad1da93c168cbf3cff30c273/Dashboard.png)" width="480"> | <img src="[screenshots/frontend-1.png](https://github.com/Varun-AI-Robotics/ledgerpilot-ai/blob/41beb77bd3acada2ad1da93c168cbf3cff30c273/AI%20Assistant.png)" width="480"> |
| <img src="[screenshots/backend-2.png](https://github.com/Varun-AI-Robotics/ledgerpilot-ai/blob/41beb77bd3acada2ad1da93c168cbf3cff30c273/Swagger.png)" width="480"> | <img src="[screenshots/frontend-2.png](https://github.com/Varun-AI-Robotics/ledgerpilot-ai/blob/41beb77bd3acada2ad1da93c168cbf3cff30c273/Scahemas.png)" width="480"> |
| **FastAPI + Reconciliation Engine** | **React + Finance Operations UI** |

## 📄 License

This project is intended as a buildathon/demo project.
