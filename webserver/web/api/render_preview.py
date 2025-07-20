from flask import Blueprint, request, jsonify
from helpers.render_template import render_display_value

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
        
        result = render_display_value(template_str, payload_raw)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"})
