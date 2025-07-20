from jinja2 import Template, TemplateError
import json

def render_display_value(template_str, payload_raw):
    """
    Renders a template with payload. Payload is always accessible via {{payload}}
    
    Args:
        template_str (str): Jinja2 template string
        payload_raw (str): Raw payload data from MQTT simulation
    
    Returns:
        dict: {"success": bool, "result": str} or {"success": bool, "error": str}
    """
    try:
        # Try to parse as JSON first
        try:
            payload = json.loads(payload_raw)
        except (json.JSONDecodeError, TypeError):
            # If parsing fails, use raw value
            payload = payload_raw
        
        # Render with Jinja2
        template = Template(template_str)
        result = template.render(payload=payload)
        return {"success": True, "result": result}
        
    except TemplateError as e:
        return {"success": False, "error": f"Template error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Render error: {str(e)}"}
