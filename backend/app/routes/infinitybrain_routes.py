from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from ..routes.auth_routes import role_required
from ..services.orchestrator import orchestrate, call_visionaryai, call_stylesense

ib_bp = Blueprint("ib", __name__, url_prefix="/ib")

@ib_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "InfinityBrain API Gateway"}), 200

@ib_bp.route("/gateway", methods=["POST"])
@jwt_required()
@role_required("admin")  # adjust roles as you prefer (e.g., "admin", "system")
def gateway():
    data = request.get_json() or {}
    service = data.get("service")
    payload = data.get("payload", {})
    if not service:
        return jsonify({"msg": "Missing 'service'"}), 400
    try:
        mock_mode = bool(current_app.config.get("ORCHESTRATOR_MOCK_MODE", True))
        result = orchestrate({"service": service, "payload": payload}, mock_mode=mock_mode)
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"msg": str(ve)}), 400
    except Exception as e:
        current_app.logger.exception("Gateway error")
        return jsonify({"msg": "Internal error"}), 500

@ib_bp.route("/visionaryai", methods=["POST"])
@jwt_required()
@role_required("admin")
def visionaryai_direct():
    payload = request.get_json() or {}
    try:
        result = call_visionaryai(payload, trace_id="-direct-")
        return jsonify({"service": "visionaryai", "response": result}), 200
    except Exception:
        return jsonify({"msg": "Internal error"}), 500

@ib_bp.route("/stylesense", methods=["POST"])
@jwt_required()
@role_required("admin")
def stylesense_direct():
    payload = request.get_json() or {}
    try:
        result = call_stylesense(payload, trace_id="-direct-")
        return jsonify({"service": "stylesense", "response": result}), 200
    except Exception:
        return jsonify({"msg": "Internal error"}), 500
