from queue import Queue

_spawn_queue = Queue()

def enqueue_spawn(spawn_type, x, y, owner_name=None, owner_photo=None, extra=None):
    """Enqueue a spawn request to be handled on the main game thread.
    spawn_type: 'tnt', 'mega', 'nuke', etc.
    x,y: world coordinates
    extra: dict for extra options
    """
    # owner_photo is a URL string; avatar is downloaded by avatar_cache workers
    _spawn_queue.put({
        "type": spawn_type,
        "x": x,
        "y": y,
        "owner_name": owner_name,
        "owner_photo": owner_photo,
        "extra": extra or {}
    })

def get_pending_spawns(max_items=50):
    items = []
    while not _spawn_queue.empty() and len(items) < max_items:
        items.append(_spawn_queue.get())
    return items
