from pathlib import Path

import requests_cache as rqc


def init_requests_cache(expire_time):
    current_dir = Path.cwd()

    rqc.install_cache(
        cache_name=str(current_dir / "cache" / "requests_cache"),
        backend="sqlite",
        expire_after=expire_time,
    )
    print(f"Requests cache initialized,set expire time to: {expire_time}s")

