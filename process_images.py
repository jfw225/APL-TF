import os

def parse_args():
    import argparse

    # Parse command line arguments
    ap = argparse.ArgumentParser(description="Detectron2 Image Processing Pipeline")
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
    # print(args.__dict__)
    pass

if __name__ == '__main__':
    args = parse_args()
    main(args)