import json

from .. import error
from .get_model import get_model


# 根据keyword在model list中搜索模型  keyword可以是int(civitai version id或model id 但model id只允许是civitai的)或str(model name keyword)
# 返回模型内容的数组 不存在则返回空数组
def search_models(keyword, api_key=""):
    if isinstance(keyword, int):
        model = get_model(keyword, api_key)
        if model is None:
            models = []
        else:
            models = [model]
        with open("models_cache.json", "r", encoding="utf-8") as f:
            model_list = json.loads(f.read())

        for m in model_list:
            if m["third_source"] != "civitai":
                continue
            if keyword == m["civitai_model_id"]:
                models.append(m)

        return models

    elif isinstance(keyword, str):
        models = []
        with open("models_cache.json", "r", encoding="utf-8") as f:
            model_list = json.loads(f.read())

        for model in model_list:
            if keyword.lower() in model["name"].lower():
                models.append(model)

        return models

    else:
        raise error.OMNI_INFER_API_ERROR("Error keyword type: " + type(keyword))


