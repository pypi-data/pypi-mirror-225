import requests
from .. import error, tools, config
import json
import random
from typing import List


# init_images:["base64"]
def img2img(init_images: List, prompt: str, model_name: str, negative_prompt="", sampler_name="Euler a", batch_size=1
            , n_iter=1, steps=20, cfg_scale=7, seed=-1, height=512, width=512, denoising_strength=0.75
            , restore_faces=False, clip_skip=2, api_key="", sd_vae=""):

    if len(init_images) <= 0:
        raise error.OMNI_INFER_API_ERROR("Error zero init_images")
    if not 1 <= batch_size <= 8:
        raise error.OMNI_INFER_API_ERROR("Error batch size: " + str(batch_size))
    if not 1 <= n_iter <= 8:
        raise error.OMNI_INFER_API_ERROR("Error n iter: " + str(n_iter))
    if not 1 <= steps <= 50:
        raise error.OMNI_INFER_API_ERROR("Error steps: " + str(steps))
    if not 1 <= cfg_scale <= 30:
        raise error.OMNI_INFER_API_ERROR("Error cfg scale: " + str(cfg_scale))
    if seed == -1:
        seed = random.randrange(0, 2 ** 32)
    if not 0 <= seed <= 2 ** 32:
        raise error.OMNI_INFER_API_ERROR("Error seed: " + str(seed))
    if not 1 <= height <= 2048:
        raise error.OMNI_INFER_API_ERROR("Error height: " + str(height))
    if not 1 <= width <= 2048:
        raise error.OMNI_INFER_API_ERROR("Error width: " + str(width))
    if not clip_skip > 0:
        raise error.OMNI_INFER_API_ERROR("Error clip skip: " + str(clip_skip))
    if not 0.0 <= denoising_strength <= 1.0:
        raise error.OMNI_INFER_API_ERROR("Error denoising_strength: " + str(denoising_strength))

    header = {
        "Content-Type": "application/json",
        "X-Omni-Key": config.API_KEY if api_key == "" else api_key,
        "accept": "application/json"
    }

    data = {
        "init_images": init_images,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "sampler_name": sampler_name,
        "batch_size": batch_size,
        "n_iter": n_iter,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "seed": seed,
        "height": height,
        "width": width,
        "model_name": model_name,
        "denoising_strength": denoising_strength,
        "restore_faces": restore_faces,
        "clip_skip": clip_skip,
        "sd_vae": sd_vae
    }

    response = requests.post(config.endpoint + "v2/img2img", data=json.dumps(data), headers=header)
    tools.response_check(response)

    re_json = json.loads(response.content.decode("utf-8"))
    if re_json["code"] != 0:
        raise error.OMNI_INFER_API_ERROR("Img2img request return a error code: {} , error message: {}"
                                         .format(str(re_json["code"]), re_json["msg"]))

    return re_json["data"]["task_id"]


