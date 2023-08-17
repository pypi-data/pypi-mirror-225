from .get_model import get_model


# 检查模型是否可用
def check_model_available(version_id: int) -> bool:
    model = get_model(version_id)
    if model is None:
        return False

    return model["enable"] == 1

