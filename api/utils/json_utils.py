from flask import jsonify as flask_jsonify

def jsonify(*args, **kwargs):
    try:
        return flask_jsonify(*args, **kwargs)
    except TypeError as e:
        # Handle non-serializable data error
        return flask_jsonify({"error": str(e)}), 500
    except RecursionError as e:
        # Handle circular reference error
        return flask_jsonify({"error": "Circular reference error"}), 500
