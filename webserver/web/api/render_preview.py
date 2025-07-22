from flask import Blueprint, request, jsonify
from helpers.render import render_template

api_render_preview = Blueprint('render_preview', __name__)

@api_render_preview.route('/api/preview-render', methods=['POST'])
def preview_render():
    """
    API endpoint to preview template rendering with simulated payload
    
    Expected JSON payload:
    {
        "render_template": "Template string with {{payload}} variables",
        "payload": "Raw payload data (JSON string, plain text, or number)"
    }
    
    Returns:
    {
        "success": true,
        "result": "Rendered template result"
    }
    or
    {
        "success": false,
        "error": "Error description"
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
