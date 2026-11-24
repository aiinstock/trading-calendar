import re

# Context path prefix (should match CONTEXT_PATH in main.py)
BASE_PATH = "/cal"

def test_api_version(client):
    response = client.get(f"{BASE_PATH}/api/v1/version")
    assert response.status_code == 200
    assert re.search('^\\d+\\.\\d+\\.\\d+$', response.json()['version'])


def test_markets_all(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets")
    assert response.status_code == 200
    assert len(response.json()) == 66


def test_markets_one_mic(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets?mic=XNYS")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_markets_multiple_mics(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets?mic=XLON,XETR,XSTO,XSWX,XMAD")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_markets_bad_mic(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets?mic=ABCD")
    assert response.status_code == 422


def test_status_all(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/status")
    assert response.status_code == 200
    print(response.json())
    assert len(response.json()) == 66


def test_status_one_mic(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/status?mic=XNYS")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_status_multiple_mics(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/status?mic=XLON,XETR,XSTO,XSWX,XMAD")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_status_bad_mic(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/status?mic=ABCD")
    assert response.status_code == 422


def test_hours_all(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/hours?start=2024-07-03&end=2024-07-03")
    assert response.status_code == 200
    assert len(response.json()) == 66


def test_hours_one_mic(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/hours?mic=XNYS&start=2024-07-03&end=2024-07-05")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_hours_korea_regular_session_after_1998(client):
    response = client.get(
        f"{BASE_PATH}/api/v1/markets/hours?mic=XKRX&start=2026-11-20&end=2026-11-23"
    )
    assert response.status_code == 200
    hours = response.json()
    assert [row['date'] for row in hours] == ['2026-11-20', '2026-11-23']
    for row in hours:
        assert row['open_time'] == f"{row['date']}T09:00:00+09:00"
        assert row['close_time'] == f"{row['date']}T15:30:00+09:00"


def test_hours_hong_kong_modern_session_and_new_york_control(client):
    response = client.get(
        f"{BASE_PATH}/api/v1/markets/hours?mic=XHKG,XNYS&start=2026-11-20&end=2026-11-20"
    )
    assert response.status_code == 200
    hours = {row['mic']: row for row in response.json()}
    assert set(hours) == {'XHKG', 'XNYS'}
    assert hours['XHKG']['open_time'] == '2026-11-20T09:30:00+08:00'
    assert hours['XHKG']['close_time'] == '2026-11-20T16:00:00+08:00'
    assert hours['XNYS']['open_time'] == '2026-11-20T09:30:00-05:00'
    assert hours['XNYS']['close_time'] == '2026-11-20T16:00:00-05:00'


def test_hours_bad_mic(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/hours?mic=ABCD&start=2024-07-03&end=2024-07-05")
    assert response.status_code == 422


def test_hours_bad_start_date(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/hours?mic=XNYS&start=2024-06-50&end=2024-07-05")
    assert response.status_code == 422


def test_hours_bad_end_date(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/hours?mic=XNYS&start=2024-07-03&end=2024-07-50")
    assert response.status_code == 422


def test_hours_start_date_after_end_date(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/hours?mic=XNYS&start=2024-07-05&end=2024-07-03")
    assert response.status_code == 422


def test_holidays_all(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/holidays?start=2024-07-05&end=2024-07-05")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_holidays_all_no_holiday(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/holidays?start=2024-07-02&end=2024-07-02")
    assert response.status_code == 200
    assert len(response.json()) == 0    


def test_holidays_one_mic(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/holidays?mic=XNYS&start=2024-07-03&end=2024-07-03")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_holidays_multiple_mics(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/holidays?mic=XLON,XETR,XSTO,XSWX,XMAD&start=2024-06-06&end=2024-06-21")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_holidays_bad_mic(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/holidays?mic=ABCD&start=2024-07-03&end=2024-07-03")
    assert response.status_code == 422


def test_holidays_bad_start_date(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/holidays?mic=XNYS&start=2024-06-50&end=2024-07-03")
    assert response.status_code == 422


def test_holidays_bad_end_date(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/holidays?mic=XNYS&start=2024-07-03&end=2024-07-50")
    assert response.status_code == 422


def test_holidays_start_date_after_end_date(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/holidays?mic=XNYS&start=2024-07-04&end=2024-07-03")
    assert response.status_code == 422

def test_holidays_get_holiday_name_1(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/holidays?mic=XHKG&start=2024-02-10&end=2024-02-10")
    assert response.status_code == 200

def test_holidays_get_holiday_name_2(client):
    response = client.get(f"{BASE_PATH}/api/v1/markets/holidays?mic=XKLS&start=2024-01-25&end=2024-01-25")
    assert response.status_code == 200
