from flask import Blueprint, request, jsonify
from helpers.render import render_template
from helpers.pid import read_pid_file
import os
import signal
import logging

api_other = Blueprint('api_other', __name__)

@api_other.route('/api/preview-render', methods=['POST'])
def preview_render():
    """
    API endpoint to preview template rendering with simulated payload
    
    Expected JSON payload:
    {
        "render_template": "Template string with {{payload}} variables",
        "payload": "Raw payload data (JSON string, plain text, or number)"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"})
        
        template_str = data.get('render_template', '')
        payload_raw = data.get('payload', '')

        try:
            return jsonify({
                "success": True,
                "result": render_template(template_str, payload_raw)
            })
        except Exception as e:
            return jsonify({"success": False, "error": f"Render error: {str(e)}"})
        
    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"})


@api_other.route('/api/kill-daemon', methods=['POST'])
def kill_deamon():
    try:
        pid = read_pid_file()
        if pid == None:
            return jsonify({"error": "Service not running"}), 400
        os.kill(pid, signal.SIGINT)
        return jsonify({"status": "killed", "pid": pid})
    except Exception as e:
        logging.error(f"Can not send signal to reload deamon : {e}")
        return jsonify({"error": str(e)}), 500