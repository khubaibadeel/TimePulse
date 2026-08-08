import TimePulse


def test_current_single_instance_api_is_exposed():
    assert callable(TimePulse.acquire_single_instance_mutex)
    assert callable(TimePulse.release_single_instance_mutex)
