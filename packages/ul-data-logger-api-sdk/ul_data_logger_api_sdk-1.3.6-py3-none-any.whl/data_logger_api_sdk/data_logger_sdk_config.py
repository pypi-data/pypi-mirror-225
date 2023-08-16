from typing import NamedTuple, Optional


class DataLoggerApiSdkConfig(NamedTuple):
    api_url: str
    api_token: Optional[str] = None
    cache_ttl_s: int = 3600
