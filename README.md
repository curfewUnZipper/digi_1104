fan-controller/
│
├── backend/
│   ├── main.py          # FastAPI controller
│   ├── controller.py    # EC + worker logic (optional split)
│   └── requirements.txt
│
├── frontend/
│   ├── app.py           # Streamlit UI
│   └── requirements.txt
│
├── venv/                # virtual environment
│
└── README.md


python -m venv venv


cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

cd frontend
streamlit run app.py



MOBILE ACCESS: ipconfig