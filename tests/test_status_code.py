def test_status_code(request_to_url, status_code):
    assert request_to_url.status_code == status_code
