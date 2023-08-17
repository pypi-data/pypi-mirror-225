import requests
from .. import error, tools, config
import json
import random


# controlnet_mask=-1 = don't use controlnet_mask
# 返回task_id
def txt2img(prompt: str, model_name: str, negative_prompt="", sampler_name="Euler a", batch_size=1, n_iter=1, steps=20
            , cfg_scale=7, seed=-1, height=512, width=512, restore_faces=False, clip_skip=2, using_controlnet=False
            , controlnet_model="", controlnet_module="none", controlnet_weight=1.0, controlnet_input_image="base64"
            , control_mode=0, controlnet_mask=-1, controlnet_resize_mode=0, controlnet_lowvram=False
            , controlnet_processor_res=64, controlnet_threshold_a=64, controlnet_threshold_b=64
            , controlnet_guidance_start=0.0, controlnet_guidance_end=1.0, controlnet_pixel_perfect=False, api_key=""
            , sd_vae=""):
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

    data = {
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
        "restore_faces": restore_faces,
        "clip_skip": clip_skip,
        "sd_vae": sd_vae
    }

    if using_controlnet:
        if not 0.0 <= controlnet_weight <= 2.0:
            raise error.OMNI_INFER_API_ERROR("Error controlnet weight: " + str(controlnet_weight))

        data["controlnet_units"] = [{
            "model": controlnet_model,
            "module": controlnet_module,
            "weight": controlnet_weight,
            "input_image": controlnet_input_image,
            "control_mode": control_mode,
            "resize_mode": controlnet_resize_mode,
            "lowvram": controlnet_lowvram,
            "processor_res": controlnet_processor_res,
            "threshold_a": controlnet_threshold_a,
            "threshold_b": controlnet_threshold_b,
            "guidance_start": controlnet_guidance_start,
            "guidance_end": controlnet_guidance_end,
            "pixel_perfect": controlnet_pixel_perfect
        }]

        if controlnet_mask != -1:
            data["controlnet_units"][0]["mask"] = controlnet_mask

    header = {
        "Content-Type": "application/json",
        "X-Omni-Key": config.API_KEY if api_key == "" else api_key,
        "accept": "application/json"
    }

    response = requests.post(config.endpoint + "v2/txt2img", headers=header, data=json.dumps(data))

    tools.response_check(response)

    re_json = json.loads(response.content.decode("utf-8"))

    if re_json["code"] != 0:
        raise error.OMNI_INFER_API_ERROR("Txt2img request return a error code: {} , error message: {}"
                                         .format(str(re_json["code"]), re_json["msg"]))

    return re_json["data"]["task_id"]

