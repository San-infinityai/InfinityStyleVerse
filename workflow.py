import yaml
from tasks import http_call, python_fn

TASK_MAP = {
    "http_call": http_call,
    "python_fn": python_fn,
}

def run_workflow_from_yaml(yaml_file):
    with open(yaml_file) as f:
        workflow = yaml.safe_load(f)

    results = {}
    for step in workflow.get("steps", []):
        task_type = step["type"]
        task = TASK_MAP.get(task_type)
        if not task:
            results[step["id"]] = {"error": f"Task type '{task_type}' not found"}
            continue

        args = step.get("args", [])
        kwargs = step.get("kwargs", {})

        # Include the logical fn name if available
        if "fn" in step:
            kwargs["fn"] = step["fn"]

        print(f"Queuing {step['id']} ({task_type})...")
        async_result = task.delay(*args, **kwargs)
        task_result = async_result.get()  # blocks for demo
        print(f"Result of {step['id']}: {task_result}")
        results[step["id"]] = task_result

    return results

if __name__ == "__main__":
    workflow_file = "design_to_shop.yaml"
    print("Running workflow...")
    workflow_results = run_workflow_from_yaml(workflow_file)
    print("\nWorkflow finished. Results:")
    for step_id, output in workflow_results.items():
        print(f"{step_id}: {output}")
