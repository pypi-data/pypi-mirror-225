from dataclasses import dataclass, asdict


@dataclass
class upscale_data:
    image: str
    upscaler_1: str = "R-ESRGAN 4x+"
    resize_mode: int = 0
    upscaling_resize: float = 1.0
    upscaling_resize_w: int = 512
    upscaling_resize_h: int = 512
    upscaling_crop: bool = True
    upscaler_2: str = -1
    extras_upscaler_2_visibility: float = -1
    gfpgan_visibility: float = -1
    codeformer_visibility: float = -1
    codeformer_weight: float = -1
    api_key: str = -1
    # -1 = don't use

    def dict(self):
        re = asdict(self)
        need_del = []
        for i in re:
            if re[i] == -1:
                need_del.append(i)

        for i in need_del:
            del re[i]

        return re
