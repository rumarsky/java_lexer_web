def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_api_lex_success(client):
    payload = {"code": "int x=5;", "keepСomments": False}
    r = client.post("/api/lex", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "tokens" in data and len(data["tokens"]) >= 2
    assert data["tokens"][0]["type"] == "KEYWORD"

def test_api_lex_error_422(client):
    # незакрытый комментарий
    payload = {"code": "/* oops", "keepСomments": False}
    r = client.post("/api/lex", json=payload)
    assert r.status_code == 422
    detail = r.json()["detail"]
    assert "line" in detail and "column" in detail and "message" in detail
