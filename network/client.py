import httpx
timeout = httpx.Timeout(
    connect=5.0,
    read=60.0,
    write=60.0,
    pool=5.0,
)
client = httpx.AsyncClient(timeout=timeout)