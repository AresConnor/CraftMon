from pathlib import Path

import requests_cache as rqc


def init_requests_cache():
    current_dir = Path.cwd()

    rqc.install_cache(
        cache_name=str(current_dir / "cache" / "requests_cache"),
        backend="sqlite",
        expire_after=60 * 5,
    )

