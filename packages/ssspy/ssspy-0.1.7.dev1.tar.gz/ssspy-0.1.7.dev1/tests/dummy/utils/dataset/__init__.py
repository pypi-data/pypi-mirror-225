import hashlib
import os
from typing import Tuple

import numpy as np

from ssspy.utils.dataset import download_sample_speech_data as _download


def download_sample_speech_data(
    sisec2010_root: str = "./tests/.data/SiSEC2010",
    mird_root: str = "./tests/.data/MIRD",
    n_sources: int = 3,
    sisec2010_tag: str = "dev1_female3",
    max_duration: float = 10,
    conv: bool = True,
    cache_dir: str = ".tests/.data/.cache",
) -> Tuple[np.ndarray, int]:
    hash = hashlib.sha256(sisec2010_root.encode("utf-8")).hexdigest()
    hash += hashlib.sha256(mird_root.encode("utf-8")).hexdigest()
    hash += hashlib.sha256(str(n_sources).encode("utf-8")).hexdigest()
    hash += hashlib.sha256(sisec2010_tag.encode("utf-8")).hexdigest()
    hash += hashlib.sha256(str(max_duration).encode("utf-8")).hexdigest()
    hash += hashlib.sha256(str(conv).encode("utf-8")).hexdigest()

    # because concatenated hash is too long
    hash = hashlib.sha256(hash.encode("utf-8")).hexdigest()

    npz_path = os.path.join(cache_dir, "{}.npz".format(hash))

    if os.path.exists(npz_path):
        npz = np.load(npz_path)
        waveform_src_img, sample_rate = npz["waveform_src_img"], npz["sample_rate"]
        sample_rate = sample_rate.item()
    else:
        waveform_src_img, sample_rate = _download(
            sisec2010_root=sisec2010_root,
            mird_root=mird_root,
            n_sources=n_sources,
            sisec2010_tag=sisec2010_tag,
            max_duration=max_duration,
            conv=conv,
        )
        os.makedirs(cache_dir, exist_ok=True)
        np.savez(npz_path, waveform_src_img=waveform_src_img, sample_rate=sample_rate)

    return waveform_src_img, sample_rate
