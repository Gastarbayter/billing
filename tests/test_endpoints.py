
def test_healthcheck(client):
    response = client.get('/v1/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}
