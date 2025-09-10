from backend.celery_app import celery_app
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor, TimeoutError

logger = logging.getLogger(__name__)

def safe_exec(user_func, args=None, kwargs=None, timeout=5):
    args = args or []
    kwargs = kwargs or {}

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(user_func, *args, **kwargs)
        try:
            result = future.result(timeout=timeout)
            return {"success": True, "result": result, "error": None}
        except TimeoutError:
            logger.error("Function execution timed out")
            return {"success": False, "result": None, "error": "Timeout"}
        except Exception:
            error_msg = traceback.format_exc()
            logger.error(f"Function execution error: {error_msg}")
            return {"success": False, "result": None, "error": error_msg}

@celery_app.task(
    bind=True,
    name="backend.app.tasks.python_fn.python_fn",
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=2,
    time_limit=30,
    soft_time_limit=25,
    queue="cpu",
)
def python_fn(self, func_code: str, func_args=None, func_kwargs=None):
    func_args = func_args or []
    func_kwargs = func_kwargs or {}
    local_scope = {}

    try:
        exec(func_code, {}, local_scope)
        user_func = local_scope.get("user_func")
        if not user_func:
            return {"success": False, "result": None, "error": "No function named 'user_func' found"}

        return safe_exec(user_func, func_args, func_kwargs, timeout=5)
    except Exception:
        error_msg = traceback.format_exc()
        logger.error(f"Error parsing function: {error_msg}")
        return {"success": False, "result": None, "error": error_msg}
