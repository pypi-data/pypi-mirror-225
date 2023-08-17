import requests
from .. import config
from .. import tools
import json
from .. import error


# 通过civitai version id获取model详细信息  模型不存在会返回null
def get_model(version_id: int, api_key=""):

    header = {
        "Content-Type": "application/json",
        "X-Omni-Key": config.API_KEY if api_key == "" else api_key
    }

    response = requests.get(config.endpoint + "v2/model/civitai_version_id/" + str(version_id), headers=header)
    tools.response_check(response)
    response_json = json.loads(response.content.decode("utf-8"))
    if response_json["code"] != 0:
        raise error.OMNI_INFER_API_ERROR("Get model request return a error code: {} , error message: {}"
                                         .format(str(response_json["code"]), response_json["msg"]))
    return response_json["data"]["model"]


