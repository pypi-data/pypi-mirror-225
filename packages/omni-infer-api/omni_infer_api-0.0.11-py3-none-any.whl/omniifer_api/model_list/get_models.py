import requests
from .. import config
from .. import tools


# 请求获取models的api并返回内容
def get_models(api_key="") -> str:

    header = {
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json",
        "X-Omni-Key": config.API_KEY if api_key == "" else api_key
    }

    response = requests.get(config.endpoint + "v2/models", headers=header)
    tools.response_check(response)
    return response.content.decode("utf-8")
