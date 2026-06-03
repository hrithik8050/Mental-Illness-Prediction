"""Unit tests for the prediction pipeline."""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from predictor import preprocess, align_features, LABEL_ENCODED_FEATURES


SAMPLE_INPUT = {
    "Age Group": "ADULT",
    "Household Composition": "LIVES ALONE",
    "Special Education Services": "NOT APPLICABLE",
    "No Chronic Med Condition": "NO",
    "Smokes": "NO",
    "Unknown Insurance Coverage": "NO",
    "Criminal Justice Status": "NO",
    "Program_Category": "Regular Treatment",
    "Religion_Category": "Unknown",
    "Employment_Status": "Employed",
    "Hours_Category": "Full-Time",
    "Education_Category": "Higher Education",
    "RACE": "WHITE",
    "hispanic_ethnicity": "NON-HISPANIC",
    "Living_Situation": "PRIVATE RESIDENCE",
    "Diagnosis_Summary": "NO DISORDER",
    "Mental_Disability_Summary": "NO DISABILITY",
    "Impairment_Summary": "NO PHYSICAL IMPAIRMENT",
    "Chronic_disease_Summary": "NO CHRONICAL MEDICAL CONDITION",
    "Canabis_Usage_Summary": "No use cannabis",
    "Smoking treatment_summary": "No Received Smoking Medication/counseling",
    "Service_drug_alcohol_Summary": "NO SERVICE ALCOHOL DRUG USE",
    "Other_testchronic_group_Summary": "NO, HYPERLIPIDEMIA/HIGHBLOODPRESSURE/OBESITY",
    "Heartchronic_Summary": "NO, HEART CHRONIC ILLNESS",
    "Disorder_summary": "NO DISORDER",
    "Other_Chronic_Illness_Summmary": "NO, CHRONIC ILLNESS",
    "Brainchronic_Summary": "NO, BRAIN CHRONIC ILLNESS",
    "Insured_or_Not": "Yes",
    "Has_Public_Insurance": "No",
    "Has_Private_or_Other_Insurance": "Yes",
    "Confirmed_Medicaid_Managed": "No",
    "Gender_Identity_Orientation": "Cisgender Man",
    "Receiving Cash Assistance": "No/Unknown",
}


def test_preprocess_returns_dataframe():
    df = preprocess(SAMPLE_INPUT)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1


def test_preprocess_label_encoded_features_are_numeric():
    df = preprocess(SAMPLE_INPUT)
    for feat in LABEL_ENCODED_FEATURES:
        assert feat in df.columns
        assert pd.api.types.is_numeric_dtype(df[feat]), f"{feat} should be numeric"


def test_preprocess_education_encoding():
    row = SAMPLE_INPUT.copy()
    row["Education_Category"] = "Higher Education"
    df = preprocess(row)
    assert df["Education_Category"].iloc[0] == 0  # first alphabetically


def test_align_features_adds_missing_columns():
    df = preprocess(SAMPLE_INPUT)
    expected = list(df.columns) + ["extra_col"]
    aligned = align_features(df.copy(), expected)
    assert "extra_col" in aligned.columns
    assert aligned["extra_col"].iloc[0] == 0


def test_preprocess_handles_unknown_value_gracefully():
    row = SAMPLE_INPUT.copy()
    row["Education_Category"] = "INVALID_VALUE"
    df = preprocess(row)
    assert df["Education_Category"].iloc[0] == 0
