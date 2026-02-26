def test_register_success(client):
    payload = {
        "first_name": "Abdi",
        "last_name": "Gurey",
        "email": "abdi_pytest@example.com",
        "age": 20,
        "sport": "tennis",
        "skill_level": "beginner",
        "club": "Club X",
        "password": "secret123"
    }

    res = client.post("/api/register", json=payload)

    # helpful debug if it fails
    assert res.status_code == 400, res.get_json()