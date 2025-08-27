from celery_app import celery_app
import requests
import time

# ---------- HTTP Call Task ----------
@celery_app.task
def http_call(url, method="GET", data=None, headers=None, access_token=None):
    """
    Make an HTTP request (GET/POST/PUT/DELETE).
    
    Args:
        url (str): The target API endpoint.
        method (str): HTTP method (default: GET).
        data (dict): Data for POST/PUT requests.
        headers (dict): Extra headers to include.
        access_token (str): Optional Bearer token for authorization.
    
    Returns:
        dict: Info about the request (status code, response snippet, error if any)
    """
    if headers is None:
        headers = {}

    # Add Bearer token if provided
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    try:
        response = requests.request(method, url, json=data, headers=headers, timeout=10)
        return {
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "content": response.text[:200],  # first 200 chars for safety
        }
    except Exception as e:
        return {"url": url, "error": str(e)}


# ---------- Python Function Task ----------
@celery_app.task
def python_fn(x, y, operation="add", fn=None):
    """
    Perform a simple math operation with optional logical function name.
    Simulates heavy computation for demo workflows.
    
    Args:
        x (int|float): First number
        y (int|float): Second number
        operation (str): Operation type (add, sub, mul, div)
        fn (str): Logical function name (for workflow step tracking)
    
    Returns:
        dict: Operation details and result
    """
    print(f"Running step '{fn}' with x={x}, y={y}, operation={operation}")

    time.sleep(3)  # simulate heavy computation / AI call / preview generation

    try:
        if operation == "add":
            result = x + y
        elif operation == "sub":
            result = x - y
        elif operation == "mul":
            result = x * y
        elif operation == "div":
            result = x / y if y != 0 else None
        else:
            return {"fn": fn, "error": f"Unsupported operation '{operation}'"}

        return {
            "fn": fn,
            "operation": operation,
            "x": x,
            "y": y,
            "result": result,
        }

    except Exception as e:
        return {"fn": fn, "error": str(e)}
