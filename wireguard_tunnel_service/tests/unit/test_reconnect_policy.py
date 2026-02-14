from wireguard_tunnel_service.core.reconnect_policy import ReconnectPolicy


def test_next_backoff_sec_uses_exponential_strategy() -> None:
    policy = ReconnectPolicy(base_interval_sec=10)
    assert policy.next_backoff_sec(1) == 10
    assert policy.next_backoff_sec(2) == 20
    assert policy.next_backoff_sec(3) == 40


def test_has_remaining_retry_respects_max_retries() -> None:
    policy = ReconnectPolicy(max_retries=3)
    assert policy.has_remaining_retry(0)
    assert policy.has_remaining_retry(2)
    assert not policy.has_remaining_retry(3)

