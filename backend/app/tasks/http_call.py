import urllib.parse as urlparse
import requests
import logging
from backend.celery_app import celery_app
from backend.app.utils.http_client import request as safe_request
from backend.app.utils.rate_limit import allow
from backend.app.config.settings import settings
from backend.app.tasks.utils import safe_retry
from celery import shared_task
from backend.app.tasks.decorators import instrument

logger = logging.getLogger(__name__)

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
                   json: dict | None = None, access_token: str | None = None, timeout: int | None = None):
    headers = headers or {}
    timeout = timeout or settings.HTTP_REQUEST_TIMEOUT

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    if not url:
        return {"status": None, "data": None, "error": "URL cannot be None"}

    parsed = urlparse.urlparse(url)
    host = (parsed.hostname or "").lower()
    if not host:
        return {"status": None, "data": None, "error": f"Invalid URL, host missing: {url}"}

    if not allow(host):
        return {"status": None, "data": None, "error": f"Rate limit exceeded for host: {host}"}

    try:
        resp = safe_request(
            method=method,
            url=url,
            headers=headers,
            timeout=timeout,
            **({"json": json} if json else {})
        )
        resp.raise_for_status()
        content_type = resp.headers.get("content-type", "")
        data = resp.json() if "application/json" in content_type else resp.text[:200]

        logger.info(f"HTTP call successful: {method} {url} status={resp.status_code}")
        return {"status": resp.status_code, "data": data, "error": None}

    except requests.RequestException as exc:
        logger.error(f"HTTP call failed: {exc} | URL: {url}")
        return safe_retry(self, exc)


@shared_task(name="tasks.http_call.run")
@instrument("http_call")
def http_call(url: str, method: str = "GET", **kwargs):
    from backend.app.utils import http_client

    if not url:
        return {"status": None, "data": None, "error": "URL cannot be None"}

    try:
        response = http_client.request(method, url, **kwargs)
        content_type = response.headers.get("content-type", "")
        data = response.json() if "application/json" in content_type else response.text[:200]
        return {"status": response.status_code, "data": data, "error": None}
    except Exception as e:
        logger.error(f"HTTP wrapper task failed: {e} | URL: {url}")
        return {"status": None, "data": None, "error": str(e)}
