"""Limiteur de débit en mémoire (fenêtre glissante), par clé (IP+chemin).

Suffisant pour le MVP mono-instance ; à remplacer par un store partagé (Redis) en montée
en charge. Le temps est injectable pour la testabilité.
"""
from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Callable


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: float,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.max_requests = max_requests
        self.window = window_seconds
        self._clock = clock
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        """True si la requête est autorisée ; enregistre le hit le cas échéant."""
        now = self._clock()
        bucket = self._hits[key]
        threshold = now - self.window
        while bucket and bucket[0] <= threshold:
            bucket.popleft()
        if len(bucket) >= self.max_requests:
            return False
        bucket.append(now)
        return True
