from flask import jsonify, request, make_response
from predicate_data import ETAG_VERSION, PREDICATE_JSON

def register_routes(app):
    @app.route("/api/v1/predicate")
    def get_predicate():
        etag = f'"v{ETAG_VERSION[0]}"'
        if request.headers.get("If-None-Match") == etag:
            return "", 304
        response = make_response(jsonify(PREDICATE_JSON[0]))
        response.headers["ETag"] = etag
        return response
