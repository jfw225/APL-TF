from torch.cuda import is_available

from detectron2.config import get_cfg, CfgNode


def setup_cfg(config_file, weights_file=None, config_opts=[],
              confidence_threshold=None, cpu=False) -> CfgNode:
    # Load config from file and command-line arguments
    cfg = get_cfg()
    cfg.merge_from_file(config_file)
    cfg.merge_from_list(config_opts)

    if confidence_threshold is not None:
        # Set score_threshold for builtin models

        cfg.MODEL.RETINANET.SCORE_THRESH_TEST = confidence_threshold
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = confidence_threshold
        cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = confidence_threshold

    if weights_file is not None:
        cfg.MODEL.WEIGHTS = weights_file

    if cpu or not is_available():
        cfg.MODEL.DEVICE = "cpu"

    cfg.freeze()

    return cfg
