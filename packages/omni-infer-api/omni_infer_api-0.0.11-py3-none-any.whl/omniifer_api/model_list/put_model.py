import json
from .. import tools
import requests
from .. import config
from .. import error


def put_model(version_id: int, api_key=""):

    header = {
        "Content-Type": "application/json",
        "X-Omni-Key": config.API_KEY if api_key == "" else api_key
    }

    data = json.dumps([version_id], ensure_ascii=False)

    response = requests.post(config.endpoint + "v2/model", headers=header, data=data)
    tools.response_check(response)

    re_json = json.loads(response.content.decode("utf-8"))

    if re_json["code"] != 0:
        raise error.OMNI_INFER_API_ERROR("Put model request return a error code: {}, error message: {}"
                                         .format(str(re_json["code"]), re_json["msg"]))

