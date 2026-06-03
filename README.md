# Mental Health Risk Prediction Tool

A machine-learning web application that predicts mental health risk based on
demographic, socioeconomic, and clinical data from the NYC Office of Mental Health (OMH).

---

## Features

- **4 ML models** — Random Forest, Decision Tree, Logistic Regression, Neural Network (MLP)
- **33 risk factors** — demographics, chronic conditions, substance use, insurance, housing, and more
- **Real-time predictions** with confidence scores and risk probability
- **Responsive UI** — works on desktop and mobile

---

## Project Structure

```
Mental-Illness-Prediction/
├── app.py                  # Flask application & routes
├── predictor.py            # Feature encoding & model inference
├── config.py               # Environment-specific configuration
├── requirements.txt        # Python dependencies
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── form.html
│   ├── about.html
│   ├── 404.html
│   └── 500.html
├── static/
│   ├── css/style.css       # Application styles
│   └── js/main.js          # Client-side validation
├── MODELS/                 # Trained model .pkl files
├── notebooks/              # EDA & model training notebooks
├── tests/                  # Pytest test suite
└── .github/workflows/ci.yml
```

---

## Quick Start

### 1. Clone and set up environment

```bash
git clone https://github.com/hrithik8050/mental-illness-prediction.git
cd mental-illness-prediction
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set a strong SECRET_KEY in production
```

### 3. Add model files

Place the trained `.pkl` files in the `MODELS/` directory:

```
MODELS/
├── best_randomforest_model.pkl
├── best_decision_tree.pkl
├── best_lr_model.pkl
└── best_mlp_model_model.pkl
```

### 4. Run the application

```bash
FLASK_ENV=development python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Running Tests

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ -v --cov=. --cov-report=html
```

---

## Models

| Model | File | Notes |
|---|---|---|
| Random Forest | `best_randomforest_model.pkl` | Best overall accuracy |
| Decision Tree | `best_decision_tree.pkl` | Interpretable |
| Logistic Regression | `best_lr_model.pkl` | Fast baseline |
| Neural Network (MLP) | `best_mlp_model_model.pkl` | Non-linear patterns |

All models were trained using scikit-learn with hyperparameter tuning via `GridSearchCV`.
Categorical features are preprocessed with one-hot encoding; ordinal features use label encoding.

---

## Data

Source: **NYC Office of Mental Health** population health dataset.
Features cover age, household composition, education, employment, housing situation,
insurance status, chronic medical conditions, substance use, criminal justice involvement,
and gender identity. Target variable: binary mental illness diagnosis indicator.

---

## Disclaimer

> **This tool is for research and educational purposes only.**
> Predictions must not be used as a substitute for professional clinical assessment or diagnosis.
> Always consult a qualified mental health professional.

---

## License

MIT
