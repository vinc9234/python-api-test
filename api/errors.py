from connexion import ProblemException, problem
from flask import Response


def handle_write_error(e):
    p = problem(status=422, title="Unsupported payload", detail=e.args[0])
    return Response(status=p.status_code, response=p.body, mimetype=p.content_type)
