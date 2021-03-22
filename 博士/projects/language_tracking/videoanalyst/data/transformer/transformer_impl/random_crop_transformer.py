from typing import Dict
import cv2
from videoanalyst.data.utils.crop_track_pair import crop_track_pair

from ..transformer_base import TRACK_TRANSFORMERS, TransformerBase


@TRACK_TRANSFORMERS.register
class RandomCropTransformer(TransformerBase):
    r"""
    Cropping training pair with data augmentation (random shift / random scaling)

    Hyper-parameters
    ----------------

    context_amount: float
        the context factor for template image
    max_scale: float
        the max scale change ratio for search image
    max_shift:  float
        the max shift change ratio for search image
    max_scale_temp: float
        the max scale change ratio for template image
    max_shift_temp:  float
        the max shift change ratio for template image
    z_size: int
        output size of template image
    x_size: int
        output size of search image
    """
    default_hyper_params = dict(
        context_amount=0.5,
        max_scale=0.3,
        max_shift=0.4,
        max_scale_temp=0.0,
        max_shift_temp=0.0,
        z_size=127,
        x_size=303,
    )

    def __init__(self, seed: int = 0) -> None:
        super(RandomCropTransformer, self).__init__(seed=seed)

    def __call__(self, sampled_data: Dict) -> Dict:
        r"""
        sampled_data: Dict()
            input data
            Dict(data1=Dict(image, anno), data2=Dict(image, anno))
        """
        CROP = False
        IM_WIDTH = 1024
        IM_HEIGHT = 768

        data1 = sampled_data["data1"]
        data2 = sampled_data["data2"]
        im_temp, bbox_temp = data1["image"], data1["anno"]
        im_curr, bbox_curr = data2["image"], data2["anno"]
        im_z, bbox_z, im_x, bbox_x, _, _ = crop_track_pair(
            im_temp,
            bbox_temp,
            im_curr,
            bbox_curr,
            config=self._hyper_params,
            rng=self._state["rng"])

        if not CROP:
            im_h, im_w = im_curr.shape[:2]
            im_x = cv2.resize(im_curr, (IM_WIDTH, IM_HEIGHT))
            scale_x = IM_WIDTH / im_w
            scale_y = IM_HEIGHT / im_h
            bbox_x = bbox_curr
            bbox_x[0] *= scale_x
            bbox_x[1] *= scale_y
            bbox_x[2] *= scale_x
            bbox_x[3] *= scale_y

        sampled_data["data1"] = dict(image=im_z, anno=bbox_z, nlp=data1['nlp'])
        sampled_data["data2"] = dict(image=im_x, anno=bbox_x, nlp=data2['nlp'])

        return sampled_data
