from datetime import datetime
from typing import Any


def success(data: Any = None) -> tuple[dict, int]:
    if data is None:
        return {"message": "success"}, 200
    return {
        "message": "success",
        "data": data,
        "datetime": datetime.utcnow().isoformat(),
    }, 200


def failure() -> tuple[dict, int]:
    return {"message": "failure"}, 500