from . import get_models
import json
from .. import error


# 更新model list缓存
def update(api_key=""):
    model_list = get_models.get_models(api_key)
    model_list_json = json.loads(model_list)
    if model_list_json["code"] != 0:
        raise error.OMNI_INFER_API_ERROR("Update request return a error code: {} , error message: {}".format(
            str(model_list_json["code"]), model_list_json["msg"]))
    with open("models_cache.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(model_list_json["data"]["models"], ensure_ascii=False))


