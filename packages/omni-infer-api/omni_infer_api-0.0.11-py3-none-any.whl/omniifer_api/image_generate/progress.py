import requests
import json
from .. import error, tools, config


# status: 0 init 1 progressing 2 success 3 failed 4 timeout
def progress(task_id: str, api_key=""):

    header = {
        "accept": "application/json",
        "X-Omni-Key": config.API_KEY if api_key == "" else api_key
    }

    response = requests.get(config.endpoint + "v2/progress?task_id=" + task_id, headers=header)
    tools.response_check(response)

    re_json = json.loads(response.content.decode("utf-8"))

    if re_json["code"] != 0:
        raise error.OMNI_INFER_API_ERROR("Progress request return a error code: {} , error message: {}"
                                         .format(str(re_json["code"]), re_json["msg"]))

    return re_json["data"]


