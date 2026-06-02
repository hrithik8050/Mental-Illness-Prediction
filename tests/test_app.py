"""Basic integration tests for the Flask application."""

import pytest

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app as flask_app


@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = False
    with flask_app.test_client() as c:
        yield c


def test_index_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_form_get_returns_200(client):
    resp = client.get("/predict")
    assert resp.status_code == 200


def test_about_returns_200(client):
    resp = client.get("/about")
    assert resp.status_code == 200


def test_404_returns_404(client):
    resp = client.get("/nonexistent-page")
    assert resp.status_code == 404


def test_form_post_missing_fields_shows_error(client):
    resp = client.post("/predict", data={"model_choice": "logistic_regression"})
    assert resp.status_code == 200
    assert b"Error" in resp.data or b"error" in resp.data.lower()


def test_form_contains_all_fields(client):
    resp = client.get("/predict")
    assert b"Age Group" in resp.data
    assert b"Education" in resp.data
    assert b"Gender" in resp.data
