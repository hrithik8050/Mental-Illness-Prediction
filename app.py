import logging
import os

from flask import Flask, render_template, request

from config import config
from predictor import predict

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
env = os.environ.get("FLASK_ENV", "default")
app = Flask(__name__)
app.config.from_object(config[env])

# ---------------------------------------------------------------------------
# Field definitions  (label, original-feature-name, options)
# ---------------------------------------------------------------------------
FIELDS = [
    ("Age Group",                     "Age Group",                     ["ADULT", "CHILD", "UNKNOWN"]),
    ("Household Composition",         "Household Composition",         ["COHABITATES WITH OTHERS", "LIVES ALONE", "NOT APPLICABLE", "UNKNOWN"]),
    ("Special Education Services",    "Special Education Services",    ["NOT APPLICABLE", "YES", "NO", "UNKNOWN"]),
    ("No Chronic Med Condition",      "No Chronic Med Condition",      ["YES", "NO", "UNKNOWN"]),
    ("Smokes",                        "Smokes",                        ["NO", "YES", "UNKNOWN"]),
    ("Unknown Insurance Coverage",    "Unknown Insurance Coverage",    ["NO", "YES"]),
    ("Criminal Justice Status",       "Criminal Justice Status",       ["NO", "YES", "UNKNOWN"]),
    ("Program Category",              "Program_Category",              ["Regular Treatment", "Extra Help", "Urgent Care"]),
    ("Religion Category",             "Religion_Category",             ["Unknown", "Formal Religion", "Spiritual but not Religious"]),
    ("Employment Status",             "Employment_Status",             ["Employed", "Not in Labor Force", "Unemployed", "Unknown"]),
    ("Working Hours",                 "Hours_Category",                ["Part-Time", "Full-Time", "Unknown"]),
    ("Education Level",               "Education_Category",            ["Higher Education", "Secondary Education", "Unknown", "Primary Education", "No Formal Education"]),
    ("Race",                          "RACE",                          ["WHITE", "OTHER/MULTIRACIAL", "BLACK", "UNKNOWN"]),
    ("Hispanic Ethnicity",            "hispanic_ethnicity",            ["HISPANIC", "NON-HISPANIC", "UNKNOWN"]),
    ("Living Situation",              "Living_Situation",              ["PRIVATE RESIDENCE", "OTHER", "INSTITUTIONAL/UNKNOWN"]),
    ("Primary Diagnosis",             "Diagnosis_Summary",             ["MENTAL ILLNESS", "NO DISORDER", "NO ADDITIONAL DIAGNOSIS", "NOT MI/DEVELOPMENT/ORGANIC/SUBSTANCEADDICTIVE/DISORDER", "UNKNOWN"]),
    ("Intellectual/Developmental Disability", "Mental_Disability_Summary", ["NO DISABILITY", "INTELECTUAL/AUTISM/DEVELOP DISABILITY", "UNKNOWN"]),
    ("Physical Impairment",           "Impairment_Summary",            ["NO PHYSICAL IMPAIRMENT", "PHYSICAL IMPAIRMENT", "UNKNOWN"]),
    ("Chronic Medical Condition",     "Chronic_disease_Summary",       ["NO CHRONICAL MEDICAL CONDITION", "CHRONICAL MEDICAL CONDITION"]),
    ("Cannabis Usage",                "Canabis_Usage_Summary",         ["No use cannabis", "Use Cannabis Medical/recreational", "UNKNOWN"]),
    ("Smoking Treatment",             "Smoking treatment_summary",     ["No Received Smoking Medication/counseling", "Received Smoking Medication/counseling", "UNKNOWN"]),
    ("Alcohol/Drug Services",         "Service_drug_alcohol_Summary",  ["NO SERVICE ALCOHOL DRUG USE", "SERVICE ALCOHOL DRUG USE", "UNKNOWN"]),
    ("Hyperlipidemia/High BP/Obesity","Other_testchronic_group_Summary",["NO, HYPERLIPIDEMIA/HIGHBLOODPRESSURE/OBESITY", "YES, HYPERLIPIDEMIA/HIGHBLOODPRESSURE/OBESITY", "UNKNOWN"]),
    ("Heart Chronic Illness",         "Heartchronic_Summary",          ["NO, HEART CHRONIC ILLNESS", "YES, HEART CHRONIC ILLNESS", "UNKNOWN"]),
    ("Alcohol/Drug Disorder",         "Disorder_summary",              ["NO DISORDER", "ALCOHOL/DRUG DISORDER", "UNKNOWN"]),
    ("Other Chronic Illness",         "Other_Chronic_Illness_Summmary",["NO, CHRONIC ILLNESS", "YES, CHRONIC ILLNESS"]),
    ("Brain Chronic Illness",         "Brainchronic_Summary",          ["NO, BRAIN CHRONIC ILLNESS", "YES, BRAIN CHRONIC ILLNESS", "UNKNOWN"]),
    ("Insured",                       "Insured_or_Not",                ["Yes", "No"]),
    ("Public Insurance",              "Has_Public_Insurance",          ["Yes", "No"]),
    ("Private / Other Insurance",     "Has_Private_or_Other_Insurance",["No", "Yes"]),
    ("Confirmed Medicaid Managed",    "Confirmed_Medicaid_Managed",    ["Yes", "No"]),
    ("Gender Identity",               "Gender_Identity_Orientation",   ["Cisgender Man", "Cisgender Woman", "Transgender Woman", "Unknown", "Transgender Man", "Transgender (Unspecified)"]),
    ("Receiving Cash Assistance",     "Receiving Cash Assistance",     ["No/Unknown", "Yes"]),
]

MODEL_CHOICES = [
    ("random_forest",      "Random Forest"),
    ("decision_tree",      "Decision Tree"),
    ("logistic_regression","Logistic Regression"),
    ("neural_network",     "Neural Network (MLP)"),
]

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def prediction_form():
    result = None
    error = None
    submitted_values = {}
    selected_model = "random_forest"

    if request.method == "POST":
        selected_model = request.form.get("model_choice", "random_forest")
        submitted_values = {feat: request.form.get(feat, "") for _, feat, _ in FIELDS}

        missing = [label for label, feat, _ in FIELDS if not submitted_values.get(feat)]
        if missing:
            error = f"Please fill in all fields. Missing: {', '.join(missing[:3])}{'...' if len(missing) > 3 else ''}."
        else:
            try:
                result = predict(submitted_values, selected_model, app.config["MODELS_DIR"])
                logger.info("Prediction: %s | model=%s", result["label"], selected_model)
            except Exception as exc:
                logger.exception("Prediction failed")
                error = f"Prediction error: {exc}"

    return render_template(
        "form.html",
        fields=FIELDS,
        values=submitted_values,
        result=result,
        error=error,
        model_choices=MODEL_CHOICES,
        selected_model=selected_model,
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    logger.error("500 error: %s", e)
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
