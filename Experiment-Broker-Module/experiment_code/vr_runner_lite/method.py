import importlib
import traceback

from datetime import datetime


def execute(module: str, func: str, arguments: dict[str], tolerance):
    status_str = {True: "succeeded", False: "failed"}
    success = False
    start_time = datetime.utcnow()

    mod = importlib.import_module(module)
    exec_func = getattr(mod, func)

    try:
        results = exec_func(*arguments)
        success = True
    except Exception as e:
        results = traceback.format_exc()

    end_time = datetime.utcnow()
    duration = end_time - start_time
    return_data = {
        "start": start_time.isoformat(),
        "end": end_time,
        "status": status_str[success],
        "duration": duration.total_seconds(),
        "output": results,
    }
    if tolerance:
        return_data["tolerance_met" : results == tolerance]
    return return_data
