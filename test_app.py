from app import app

def test_bmi_normal():
    client = app.test_client()
    res = client.get('/bmi?weight=70&height=1.75')
    assert res.status_code == 200
    data = res.get_json()
    assert data["bmi"] == 22.86
    assert data["category"] == "Normal weight"

def test_bmi_overweight():
    client = app.test_client()
    res = client.get('/bmi?weight=85&height=1.75')
    assert res.status_code == 200
    assert res.get_json()["category"] == "Overweight"

def test_bmi_invalid():
    client = app.test_client()
    res = client.get('/bmi?weight=-5&height=1.75')
    assert res.status_code == 400

def test_health():
    client = app.test_client()
    res = client.get('/health')
    assert res.status_code == 200
