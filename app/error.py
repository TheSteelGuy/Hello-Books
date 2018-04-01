from flask import jsonify


def resource_not_found(error):
    """resource not found"""
    response = jsonify({"message": "the resource does not exist"})
    response.status_code = 404
    return response


def server_error(error):
    """Handle 500 error."""
    response = jsonify({
        "message":"Internal server error"
    })
    response.status_code = 500
    return response


def method_not_allowed(error):
    """Handle 405 error."""
    response = jsonify({"message": "Method not allowed"})
    response.status_code = 405
    return response
