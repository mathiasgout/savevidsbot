from api.tools import basic_tools


def test_get_timestamp_utc():
    assert isinstance(basic_tools.get_timestamp_utc(), int)
    assert basic_tools.get_timestamp_utc() > 1640995200  # 2022/01/01 00:00:00
