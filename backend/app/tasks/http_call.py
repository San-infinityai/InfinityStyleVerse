import urllib.parse as urlparse
import requests
from backend.celery_app import celery_app
from backend.app.utils.http_client import request as safe_request
from backend.app.utils.rate_limit import allow
from backend.app.config.settings import settings
from celery import shared_task
from backend.app.tasks.decorators import instrument


@celery_app.task(
    bind=True,
    name="backend.app.tasks.http_call.http_call_task",
    autoretry_for=(requests.RequestException,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=3,
    time_limit=30,
    soft_time_limit=25,
    queue="io",
)
def http_call_task(self, url: str, method: str = "GET", headers: dict | None = None,
                   json: dict | None = None, access_token: str | None = None):
    """Celery task to make an HTTP request safely."""
    headers = headers or {}

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    # Extract host
    if not url:
        raise ValueError("URL cannot be None")
    parsed = urlparse.urlparse(url)
    host = (parsed.hostname or "").lower()
    if not host:
        raise ValueError(f"Invalid URL, host missing: {url}")

    if not allow(host):
        raise RuntimeError(f"Rate limit exceeded for host: {host}")

    try:
        resp = safe_request(
            method=method,
            url=url,
            headers=headers,
            timeout=settings.HTTP_REQUEST_TIMEOUT,
            **({"json": json} if json else {})
        )
        resp.raise_for_status()
        content_type = resp.headers.get("content-type", "")
        data = resp.json() if "application/json" in content_type else resp.text[:200]
        return {"status": resp.status_code, "data": data}

    except requests.RequestException as exc:
        raise self.retry(exc=exc)


@shared_task(name="tasks.http_call.run")
@instrument("http_call")
def http_call(url: str, method: str = "GET", **kwargs):
    """Shared task / wrapper to make HTTP requests."""
    from backend.app.utils import http_client

    if not url:
        raise ValueError("URL cannot be None")

    response = http_client.request(method, url, **kwargs)
    content_type = response.headers.get("content-type", "")
    data = response.json() if "application/json" in content_type else response.text[:200]
    return {"status": response.status_code, "data": data}
