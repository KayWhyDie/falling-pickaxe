import threading
from queue import Queue
import requests
from io import BytesIO
import pygame

_cache = {}
_pending = set()
_queue = Queue()
_WORKER_COUNT = 2


def _worker():
    while True:
        url = _queue.get()
        if url is None:
            break
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = BytesIO(resp.content)
            # Use pygame.image.load which can read file-like
            surf = pygame.image.load(data).convert_alpha()
            # scale to 32x32 for avatars
            surf = pygame.transform.scale(surf, (32, 32))
            _cache[url] = surf
        except Exception:
            _cache[url] = None
        finally:
            _pending.discard(url)
            _queue.task_done()


# Start workers
for _ in range(_WORKER_COUNT):
    t = threading.Thread(target=_worker, daemon=True)
    t.start()


def request(url):
    """Request download of avatar for url in background. Non-blocking."""
    if not url:
        return
    if url in _cache or url in _pending:
        return
    _pending.add(url)
    _queue.put(url)


def get(url):
    """Return cached pygame.Surface or None if not available yet or failed."""
    return _cache.get(url, None)


def clear():
    _cache.clear()


# For clean shutdown (not strictly required)
def shutdown():
    for _ in range(_WORKER_COUNT):
        _queue.put(None)
