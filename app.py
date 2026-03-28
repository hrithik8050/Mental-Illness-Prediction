from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

FIELDS = [
    ("Age Group", ["ADULT", "CHILD", "UNKNOWN"]),
    ("Household Composition", ["COHABITATES WITH OTHERS", "LIVES ALONE", "NOT APPLICABLE", "UNKNOWN"]),
    ("Special Education Services", ["NOT APPLICABLE", "YES", "NO", "UNKNOWN"]),
  
    ("No Chronic Med Condition", ["YES", "NO", "UNKNOWN"]),
    ("Smokes", ["NO", "YES", "UNKNOWN"]),
    ("Unknown Insurance Coverage", ["NO", "YES"]),
    ("Criminal Justice Status", ["NO", "YES", "UNKNOWN"]),
    ("Program_Category", ["Regular Treatment", "Extra Help", "Urgent Care"]),
    ("Religion_Category", ["Unknown", "Formal Religion", "Spiritual but not Religious"]),
    ("Employment_Status", ["Employed", "Not in Labor Force", "Unemployed", "Unknown"]),
    ("Hours_Category", ["Part-Time", "Full-Time", "Unknown"]),
    ("Education_Category", [
        "Higher Education", "Secondary Education", "Unknown",
        "Primary Education", "No Formal Education"
    ]),
    ("RACE", ["WHITE", "OTHER/MULTIRACIAL", "BLACK", "UNKNOWN"]),
    ("hispanic_ethnicity", ["HISPANIC", "NON-HISPANIC", "UNKNOWN"]),
    ("Living_Situation", ["PRIVATE RESIDENCE", "OTHER", "INSTITUTIONAL/UNKNOWN"]),
    ("Diagnosis_Summary", [
        "MENTAL ILLNESS", "NO DISORDER", "NO ADDITIONAL DIAGNOSIS",
        "NOT MI/DEVELOPMENT/ORGANIC/SUBSTANCEADDICTIVE/DISORDER", "UNKNOWN"
    ]),
    ("Mental_Disability_Summary", [
        "NO DISABILITY", "INTELECTUAL/AUTISM/DEVELOP DISABILITY", "UNKNOWN"
    ]),
    ("Impairment_Summary", ["NO PHYSICAL IMPAIRMENT", "PHYSICAL IMPAIRMENT", "UNKNOWN"]),
    ("Chronic_disease_Summary", ["NO CHRONICAL MEDICAL CONDITION", "CHRONICAL MEDICAL CONDITION"]),
    ("Canabis_Usage_Summary", ["No use cannabis", "Use Cannabis Medical/recreational", "UNKNOWN"]),
    ("Smoking treatment_summary", [
        "No Received Smoking Medication/counseling",
        "Received Smoking Medication/counseling", "UNKNOWN"
    ]),
    ("Service_drug_alcohol_Summary", [
        "NO SERVICE ALCOHOL DRUG USE", "SERVICE ALCOHOL DRUG USE", "UNKNOWN"
    ]),
    ("Other_testchronic_group_Summary", [
        "NO, HYPERLIPIDEMIA/HIGHBLOODPRESSURE/OBESITY",
        "YES, HYPERLIPIDEMIA/HIGHBLOODPRESSURE/OBESITY", "UNKNOWN"
    ]),
    ("Heartchronic_Summary", [
        "NO, HEART CHRONIC ILLNESS", "YES, HEART CHRONIC ILLNESS", "UNKNOWN"
    ]),
    ("Disorder_summary", ["NO DISORDER", "ALCOHOL/DRUG DISORDER", "UNKNOWN"]),
    ("Other_Chronic_Illness_Summmary", ["NO, CHRONIC ILLNESS", "YES, CHRONIC ILLNESS"]),
    ("Brainchronic_Summary", [
        "NO, BRAIN CHRONIC ILLNESS", "YES, BRAIN CHRONIC ILLNESS", "UNKNOWN"
    ]),
    ("Insured_or_Not", ["Yes", "No"]),
    ("Has_Public_Insurance", ["Yes", "No"]),
    ("Has_Private_or_Other_Insurance", ["No", "Yes"]),
    ("Confirmed_Medicaid_Managed", ["Yes", "No"]),
    ("Gender_Identity_Orientation", [
        "Cisgender Man", "Cisgender Woman", "Transgender Woman", "Unknown",
        "Transgender Man", "Transgender (Unspecified)"
    ]),
    ("Receiving Cash Assistance", ["No/Unknown", "Yes"]),
]

# Map safe HTML field names
def slugify(label: str) -> str:
    return (
        label.lower()
        .replace("/", "_")
        .replace(" ", "_")
        .replace("-", "_")
        .replace("__", "_")
    )

FIELD_KEYS = [(label, slugify(label), options) for (label, options) in FIELDS]


@app.route("/")
def index():
    # Page 1 — Landing
    return render_template("index.html")


@app.route("/form", methods=["GET", "POST"])
def form():
    result_text = ""
    values = {}

    if request.method == "POST":
        # Collect submitted values
        for label, key, _opts in FIELD_KEYS:
            values[key] = request.form.get(key, "")
        # Here you could run a model; for now we simply acknowledge submission.
        result_text = "Form submitted! ({} fields captured)".format(len(values))

    return render_template(
        "form.html",
        fields=FIELD_KEYS,
        values=values,
        result=result_text
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
