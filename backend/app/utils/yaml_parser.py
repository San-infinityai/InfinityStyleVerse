import yaml
import json

# Define required schema keys
REQUIRED_KEYS = {"id", "type", "depends_on"}

def validate_workflow_yaml(yaml_str):
    """
    Validate YAML schema for a workflow.
    Must include: id, type, depends_on
    """
    try:
        data = yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")

    # Check each task
    for task in data.get("tasks", []):
        if not REQUIRED_KEYS.issubset(task.keys()):
            missing = REQUIRED_KEYS - task.keys()
            raise ValueError(f"Task missing keys: {missing}")
    return True

def yaml_to_dag(yaml_str):
    """
    Convert YAML to a DAG JSON (dictionary with task dependencies)
    """
    validate_workflow_yaml(yaml_str)
    data = yaml.safe_load(yaml_str)

    # Simple DAG representation: {task_id: depends_on_list}
    dag = {task["id"]: task["depends_on"] for task in data.get("tasks", [])}
    return json.dumps(dag, indent=2)
