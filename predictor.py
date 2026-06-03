"""Model loading and prediction logic."""

import logging
from pathlib import Path

import joblib
import pandas as pd

logger = logging.getLogger(__name__)

# Features encoded with LabelEncoder (ordinal/binary)
LABEL_ENCODED_FEATURES = {
    "Education_Category": ["Higher Education", "No Formal Education", "Primary Education", "Secondary Education", "Unknown"],
    "Unknown Insurance Coverage": ["NO", "YES"],
    "Insured_or_Not": ["No", "Yes"],
    "Receiving Cash Assistance": ["No/Unknown", "Yes"],
    "Has_Public_Insurance": ["No", "Yes"],
    "Has_Private_or_Other_Insurance": ["No", "Yes"],
    "Confirmed_Medicaid_Managed": ["No", "Yes"],
    "Chronic_disease_Summary": ["CHRONICAL MEDICAL CONDITION", "NO CHRONICAL MEDICAL CONDITION"],
    "Other_Chronic_Illness_Summmary": ["NO, CHRONIC ILLNESS", "YES, CHRONIC ILLNESS"],
}

# Features encoded with OneHotEncoder (all remaining categorical)
OHE_FEATURES = [
    "Age Group",
    "Household Composition",
    "Special Education Services",
    "No Chronic Med Condition",
    "Smokes",
    "Criminal Justice Status",
    "Program_Category",
    "Religion_Category",
    "Employment_Status",
    "Hours_Category",
    "RACE",
    "hispanic_ethnicity",
    "Living_Situation",
    "Diagnosis_Summary",
    "Mental_Disability_Summary",
    "Impairment_Summary",
    "Canabis_Usage_Summary",
    "Smoking treatment_summary",
    "Service_drug_alcohol_Summary",
    "Other_testchronic_group_Summary",
    "Heartchronic_Summary",
    "Disorder_summary",
    "Brainchronic_Summary",
    "Gender_Identity_Orientation",
]

MODEL_FILES = {
    "random_forest": "best_randomforest_model.pkl",
    "decision_tree": "best_decision_tree.pkl",
    "logistic_regression": "best_lr_model.pkl",
    "neural_network": "best_mlp_model_model.pkl",
}

_model_cache: dict = {}


def load_model(model_name: str, models_dir: Path):
    if model_name in _model_cache:
        return _model_cache[model_name]

    filename = MODEL_FILES.get(model_name)
    if not filename:
        raise ValueError(f"Unknown model: {model_name}")

    path = models_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")

    logger.info("Loading model '%s' from %s", model_name, path)
    model = joblib.load(path)
    _model_cache[model_name] = model
    return model


def preprocess(form_data: dict) -> pd.DataFrame:
    """Convert raw form values to model-ready feature vector."""
    row: dict = {}

    # Label-encoded features
    for feature, categories in LABEL_ENCODED_FEATURES.items():
        value = form_data.get(feature, "")
        try:
            row[feature] = categories.index(value)
        except ValueError:
            logger.warning("Unknown value '%s' for feature '%s'; defaulting to 0", value, feature)
            row[feature] = 0

    # One-hot encoded features — build dummy columns manually
    for feature in OHE_FEATURES:
        value = form_data.get(feature, "")
        # Find all possible options for this feature from training (via model feature names)
        # We reconstruct by checking what dummy columns exist in the model
        row[f"_ohe_{feature}"] = value  # placeholder; expanded below

    # Build a single-row DataFrame for OHE features and get_dummies
    ohe_input = {f: form_data.get(f, "") for f in OHE_FEATURES}
    ohe_df = pd.DataFrame([ohe_input])
    dummies = pd.get_dummies(ohe_df, columns=OHE_FEATURES)

    # Combine label-encoded scalar features with OHE dummies
    label_df = pd.DataFrame([{k: v for k, v in row.items() if not k.startswith("_ohe_")}])
    combined = pd.concat([label_df.reset_index(drop=True), dummies.reset_index(drop=True)], axis=1)

    return combined


def align_features(df: pd.DataFrame, expected_features: list) -> pd.DataFrame:
    """Add missing dummy columns as 0 and reorder to match training features."""
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0
    return df[expected_features]


def predict(form_data: dict, model_name: str, models_dir: Path) -> dict:
    """Return prediction label and confidence scores."""
    model = load_model(model_name, models_dir)
    features = preprocess(form_data)
    features = align_features(features, list(model.feature_names_in_))

    prediction = int(model.predict(features)[0])
    label = "At Risk of Mental Illness" if prediction == 1 else "No Mental Illness Detected"

    result = {"prediction": prediction, "label": label, "confidence": None}

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(features)[0]
        result["confidence"] = round(float(max(proba)) * 100, 1)
        result["risk_probability"] = round(float(proba[1]) * 100, 1)

    return result
