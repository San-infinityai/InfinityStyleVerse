from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..database import db
from ..models.workflow_defs import WorkflowDef
import yaml
import json
from typing import List, Dict, Tuple

bp = Blueprint("workflow_routes", __name__, url_prefix="/flow/workflows")

# ----------------------
# Helpers: validation
# ----------------------
def validate_workflow_structure(parsed: dict) -> Tuple[bool, str]:
    if not isinstance(parsed, dict):
        return False, "root of YAML must be a mapping (object)"
    if "steps" not in parsed:
        return False, "workflow must contain 'steps' key"
    steps = parsed["steps"]
    if not isinstance(steps, list):
        return False, "'steps' must be a list"
    ids = set()
    for idx, step in enumerate(steps):
        if not isinstance(step, dict):
            return False, f"each step must be a mapping; step at index {idx} is not"
        step_id = step.get("id")
        step_type = step.get("type")
        if not step_id or not isinstance(step_id, (str, int)):
            return False, f"step at index {idx} is missing an 'id' (string or int)"
        if not step_type or not isinstance(step_type, str):
            return False, f"step '{step_id}' missing 'type' (string)"
        if str(step_id) in ids:
            return False, f"duplicate step id: {step_id}"
        ids.add(str(step_id))
        depends = step.get("depends_on")
        if depends is not None and not (isinstance(depends, str) or isinstance(depends, list)):
            return False, f"'depends_on' for step {step_id} must be string or list"
    return True, ""

# ----------------------
# Helpers: DAG builder
# ----------------------
def build_dag(parsed: dict) -> Tuple[List[Dict], List[Tuple[str, str]]]:
    steps = parsed.get("steps", [])
    ids = [str(s["id"]) for s in steps]
    nodes = []
    edges = []
    id_to_step = {str(s["id"]): s for s in steps}

    for s in steps:
        sid = str(s["id"])
        nodes.append({
            "id": sid,
            "type": s.get("type"),
            "meta": {k: v for k, v in s.items() if k not in ("id", "type", "depends_on")}
        })

    for i, s in enumerate(steps):
        sid = str(s["id"])
        depends = s.get("depends_on")
        if depends is None:
            if i > 0:
                prev_id = str(steps[i-1]["id"])
                edges.append((prev_id, sid))
        else:
            depends_list = [depends] if isinstance(depends, str) else depends
            for dep in depends_list:
                dep_id = str(dep)
                if dep_id not in id_to_step:
                    raise ValueError(f"step '{sid}' depends_on unknown step '{dep_id}'")
                edges.append((dep_id, sid))

    # cycle detection (Kahn's)
    adjacency = {n["id"]: [] for n in nodes}
    indegree = {n["id"]: 0 for n in nodes}
    for a, b in edges:
        adjacency[a].append(b)
        indegree[b] += 1
    queue = [n for n in indegree if indegree[n] == 0]
    visited = 0
    while queue:
        node = queue.pop(0)
        visited += 1
        for neigh in adjacency[node]:
            indegree[neigh] -= 1
            if indegree[neigh] == 0:
                queue.append(neigh)
    if visited != len(nodes):
        raise ValueError("Cycle detected in workflow steps")

    return nodes, edges

# ----------------------
# POST /flow/workflows
# ----------------------
@bp.route("/", methods=["POST"])
@jwt_required()
def register_workflow():
    payload = request.get_json() or {}
    name = payload.get("name")
    version = payload.get("version", "1.0")
    dsl_yaml = payload.get("dsl_yaml")
    if not name or not dsl_yaml:
        return jsonify({"error": "name and dsl_yaml are required"}), 400

    try:
        parsed = yaml.safe_load(dsl_yaml)
    except yaml.YAMLError as e:
        return jsonify({"error": f"Invalid YAML: {str(e)}"}), 400

    ok, msg = validate_workflow_structure(parsed)
    if not ok:
        return jsonify({"error": f"Invalid workflow spec: {msg}"}), 400

    try:
        nodes, edges = build_dag(parsed)
    except ValueError as e:
        return jsonify({"error": f"Invalid workflow DAG: {str(e)}"}), 400

    existing = WorkflowDef.query.filter_by(name=name, version=version).first()
    if existing:
        return jsonify({"error": "workflow with same name and version exists"}), 409

    user_id = get_jwt_identity()
    wf = WorkflowDef(
        name=name,
        version=version,
        dsl_yaml=dsl_yaml,
        dag_json=json.dumps({"nodes": nodes, "edges": edges}),
        created_by=str(user_id)
    )
    db.session.add(wf)
    db.session.commit()
    return jsonify({"message": "workflow registered", "id": wf.id, "dag": {"nodes": nodes, "edges": edges}}), 201

# ----------------------
# GET list
# ----------------------
@bp.route("/", methods=["GET"])
@jwt_required()
def list_workflows():
    name = request.args.get("name")
    version = request.args.get("version")
    include_dag = request.args.get("include_dag", "false").lower() in ("1", "true", "yes")

    q = WorkflowDef.query
    if name:
        q = q.filter_by(name=name)
    if version:
        q = q.filter_by(version=version)

    items = [wf.to_dict(include_dag=include_dag) for wf in q.order_by(WorkflowDef.created_at.desc()).all()]
    return jsonify({"items": items, "count": len(items)}), 200

# ----------------------
# GET by id
# ----------------------
@bp.route("/<int:wf_id>", methods=["GET"])
@jwt_required()
def get_workflow(wf_id):
    wf = WorkflowDef.query.get_or_404(wf_id)
    include_dag = request.args.get("include_dag", "false").lower() in ("1", "true", "yes")
    return jsonify(wf.to_dict(include_dag=include_dag)), 200
