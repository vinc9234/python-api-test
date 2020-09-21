"""
Implement the API described by store.yaml OAS spec.




"""
from datetime import datetime
from uuid import uuid4

import bson
from connexion import problem
from flask import after_this_request, current_app, request


def get_item(uuid: str):
    """
    :return an object like {"uuid": "", "status": "", "item": ..} on success
            problem(status=404, title="Not Found", detail=f"uuid: {uuid}") otherwise
    Implement this @solution
    """
    i = current_app.config["store"].get(uuid)
    if not i:
        return problem(status=404, title="Not Found", detail=f"uuid: {uuid}")

    return {
        "uuid": uuid,
        "status": "success",
        "item": i,
    }


def get_items(limit: int = 10, cursor: str = ""):
    c = limit
    ret = []
    items = iter(
        x for x in sorted(current_app.config["store"].list(cursor=cursor).items())
    )
    for i in range(limit):
        try:
            o = next(items)
            k, v = o
            ret.append(v)
            c -= 1
        except StopIteration:
            break
        except ValueError as e:
            current_app.logger.error("errore: %r, %r", e, o)
    try:
        cursor = next(items)[0]
    except StopIteration:
        cursor = None
    return dict(limit=limit, count=limit - c, items=ret, cursor=cursor)


def post_items(body: dict):

    # connexion cannot validate this kind of entries
    try:
        bson.encode(body)
    except bson.InvalidDocument as e:
        return problem(status=422, title="Unprocessable Entity", detail=e.args[0])
    except OverflowError as e:
        return problem(status=422, title="Unprocessable Entity", detail=e.args[0])

    uuid = str(uuid4())
    ts = datetime.now().isoformat()
    current_app.config["store"].add(uuid, dict(id=uuid, timestamp=ts, item=body))
    return {
        "id": uuid,
        "timestamp": ts,
        "status": "success",
        "url": request.base_url + "/" + uuid,
        "debug": current_app.config["store"].list(),
    }


def get_status():
    """Ritorna lo stato dell'applicazione.

    Ritorna lo stato dell'applicazione.  # noqa: E501


    :rtype: Problem
    """

    @after_this_request
    def cache_no_store(response):
        """Add the 'no-store' cache value to avoid clients and
        intermediaries to store this response.
        """
        response.headers["Cache-Control"] = "no-store"
        return response

    if current_app.config["store"].ping():
        return problem(
            status=200,
            title="Success",
            detail="Il servizio funziona correttamente",
            ext={"result": "ok"},
        )

    return problem(
        status=503,
        title="Service Unavailable",
        detail="Questo errore viene ritornato randomicamente.",
        headers={"Retry-After": "1"},
    )
