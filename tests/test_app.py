"""
FastAPI pytest tests for Mergington High School API (AAA pattern)
"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    # (client is already arranged)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_new_student_then_reflected_in_get():
    # Arrange
    new_email = "newstudent@mergington.edu"

    # Act
    signup_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": new_email}
    )

    # Assert
    assert signup_response.status_code == 200
    get_response = client.get("/activities")
    assert new_email in get_response.json()["Chess Club"]["participants"]


def test_signup_duplicate_student_returns_400():
    # Arrange
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": duplicate_email}
    )

    # Assert
    assert response.status_code == 400


def test_delete_existing_participant_then_not_in_get():
    # Arrange
    existing_email = "daniel@mergington.edu"

    # Act
    delete_response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": existing_email}
    )

    # Assert
    assert delete_response.status_code == 200
    get_response = client.get("/activities")
    assert existing_email not in get_response.json()["Chess Club"]["participants"]


def test_delete_nonexisting_participant_returns_404():
    # Arrange
    nonexistent_email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": nonexistent_email}
    )

    # Assert
    assert response.status_code == 404


def test_remove_from_nonexistent_activity_returns_404():
    # Arrange
    bad_activity = "Nonexistent Club"

    # Act
    response = client.delete(
        f"/activities/{bad_activity}/participants",
        params={"email": "student@mergington.edu"}
    )

    # Assert
    assert response.status_code == 404
