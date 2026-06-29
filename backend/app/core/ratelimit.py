"""Limiteurs de débit par clé (IP+chemin).

- `RateLimiter` : en mémoire (fenêtre glissante), mono-instance — défaut MVP.
- `RedisRateLimiter` : compteur fenêtre fixe partagé via Redis (INCR+EXPIRE),
  pour un déploiement multi-instance.

Le temps est injectable pour la testabilité. `build_limiter()` choisit le backend
selon `settings.rate_limit_backend`.
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


class RedisRateLimiter:
    """Fenêtre fixe distribuée (INCR + EXPIRE) — compteur partagé entre instances.

    L'horloge murale (`time.time`) est utilisée pour que le découpage des fenêtres
    soit cohérent entre process/pods (la monotone n'est pas partageable).
    """

    def __init__(self, client, max_requests: int, window_seconds: float,
                 clock: Callable[[], float] = time.time) -> None:
        self.client = client
        self.max_requests = max_requests
        self.window = int(window_seconds)
        self._clock = clock

    def allow(self, key: str) -> bool:
        bucket = int(self._clock() // self.window)
        rkey = f"rl:{key}:{bucket}"
        count = int(self.client.incr(rkey))
        if count == 1:
            # TTL un peu supérieur à la fenêtre pour purger l'ancienne tranche.
            self.client.expire(rkey, self.window * 2)
        return count <= self.max_requests


def build_limiter(max_requests: int | None = None, window_seconds: float | None = None):
    """Construit le limiteur selon la configuration (mémoire par défaut, sinon Redis)."""
    from app.config import settings

    mx = settings.rate_limit_max if max_requests is None else max_requests
    win = settings.rate_limit_window_seconds if window_seconds is None else window_seconds
    if settings.rate_limit_backend == "redis":
        import redis

        client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
        return RedisRateLimiter(client, mx, win)
    return RateLimiter(mx, win)
