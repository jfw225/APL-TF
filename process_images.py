import os
from tqdm import tqdm
from multiprocessing import set_start_method

from pipeline.pipeline import Pipeline
from pipeline.image_input import ImageInput
from pipeline.async_predict import AsyncPredict
from pipeline.predict import Predict
from pipeline.seperate_background import SeperateBackground
from pipeline.annotate_image import AnnotateImage
from pipeline.image_output import ImageOutput
from pipeline.utils.detectron import setup_cfg


def parse_args():
    """ Parses command line arguments. """

    import argparse

    # Parse command line arguments
    ap = argparse.ArgumentParser(
        description="Detectron2 Image Processing Pipeline")
    ap.add_argument("-i", "--input", required=True,
                    help="path to input image file or directory")
    ap.add_argument("-o", "--output", default="output",
                    help="path to output directory (default: output)")
    ap.add_argument("-p", "--progress", action="store_true",
                    help="display progress")
    ap.add_argument("-sb", "--seperate-background", action="store_true",
                    help="seperate background")

    # Detectron Settings
    ap.add_argument("--config-file",
                    default="configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml",
                    help="path to config file (default: configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    ap.add_argument("--config-opts", default=[], nargs=argparse.REMAINDER,
                    help="modify model config options using the command-line")
    ap.add_argument("--weights-file", default=None,
                    help="path to model weights file")
    ap.add_argument("--confidence-threshold", type=float, default=0.5,
                    help="minimum score for instance predictions to be shown (default: 0.5)")

    # Mutliprocessing settings
    ap.add_argument("--gpus", type=int, default=1,
                    help="number of GPUs (default: 1)")
    ap.add_argument("--cpus", type=int, default=0,
                    help="number of CPUs (default: 1)")
    ap.add_argument("--queue-size", type=int, default=3,
                    help="queue size per process (default: 3)")
    ap.add_argument("--single-process", action="store_true",
                    help="force the pipeline to run in a single process")

    return ap.parse_args()


def main(args):
    """ The main function for image processing. """

    # Create output directory if needed
    os.makedirs(args.output, exist_ok=True)

    # Image output type
    output_type = "vis_image"

    # Create pipeline tasks
    # temporary image input for testing
    image_input = ImageInput(args.input)

    cfg = setup_cfg(config_file=args.config_file,
                    weights_file=args.weights_file,
                    config_opts=args.config_opts,
                    confidence_threshold=args.confidence_threshold,
                    cpu=False if args.gpus > 0 else True)

    if not args.single_process:
        set_start_method("spawn", force=True)
        predict = AsyncPredict(cfg,
                               num_gpus=args.gpus,
                               num_cpus=args.cpus,
                               queue_size=args.queue_size,
                               ordered=False)
    else:
        predict = Predict(cfg)

    if args.seperate_background:
        annotate_image = None
        seperate_background = SeperateBackground(output_type)
    else:
        seperate_background = None
        metadata_name = cfg.DATASETS.TEST[0] if len(
            cfg.DATASETS.TEST) else "__unused"
        annotate_image = AnnotateImage(output_type, metadata_name)

    # temp image output for testing
    image_output = ImageOutput(output_type, args.output)

    # Create the image processing pipeline
    pipeline = (image_input
                >> predict
                >> seperate_background
                >> annotate_image
                >> image_output)

    # Main Loop
    results = list()
    while image_input.is_working() or predict.is_working():
        if (result := pipeline.map(None)) != Pipeline.Empty:
            results.append(result)

    predict.cleanup()
    # print("Results: " + str(result))


if __name__ == '__main__':
    args = parse_args()
    main(args)
