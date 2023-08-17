import json

import requests

from .upscale_data import upscale_data
from .. import config
from .. import error
from PIL import Image
import base64
from io import BytesIO
from typing import Tuple
from .. import tools


def get_size(image: str) -> Tuple[int, int]:
    return Image.open(BytesIO(base64.b64decode(image))).size


def upscale(data: upscale_data):
    data = data.dict()

    if data["resize_mode"] == 1 and not 0 < data["upscaling_resize_w"] <= 2048:
        raise error.OMNI_INFER_API_ERROR("illegal value: upscaling_resize_w")
    if data["resize_mode"] == 1 and not 0 < data["upscaling_resize_h"] <= 2048:
        raise error.OMNI_INFER_API_ERROR("illegal value: upscaling_resize_h")

    if data["resize_mode"] == 0:
        width, height = get_size(data["image"])
        if not (0 < width * data["upscaling_resize"] <= 2048 and 0 < height * data["upscaling_resize"] <= 2048):
            raise error.OMNI_INFER_API_ERROR("Magnification too high: width: {} height: {}".format(width, height))

    headers = {
        "Content-Type": "application/json",
        "X-Omni-Key": config.API_KEY if "api_key" not in data else data["api_key"],
        "accept": "application/json"
    }

    True if "api_key" not in data else data.pop("api_key")

    response = requests.post(config.endpoint + "v2/upscale", headers=headers, data=json.dumps(data))
    tools.response_check(response)

    re_json = json.loads(response.content.decode("utf-8"))
    if re_json["code"] != 0:
        raise error.OMNI_INFER_API_ERROR("Upscale request return a error code: {} , error message: {}"
                                         .format(str(re_json["code"]), re_json["msg"]))

    return re_json["data"]["task_id"]

