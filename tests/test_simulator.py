"""Week 8 simulator check (Week 7 idea): retries back off, with jitter, and never wait longer than the cap."""
import random

from simulator.send_readings import backoff_delay


def test_backoff_grows_with_jitter_and_a_cap():
    random.seed(1)
    waits = [[backoff_delay(attempt) for _ in range(500)] for attempt in range(8)]
    assert all(0 <= w <= 8.0 for ws in waits for w in ws), "never wait longer than the cap (8 seconds)"
    assert max(waits[0]) <= 0.5 and max(waits[3]) > 2, "the longest possible wait should double with each attempt"
    assert len({round(w, 3) for w in waits[3]}) > 100, "add jitter: random waits, so phones do not all retry together"
