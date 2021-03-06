import argparse
import logging
import os

import torch
import torch.distributed as dist
from torch.utils.data import DataLoader

from ssd.config import cfg
from ssd.data import samplers
from ssd.data.datasets import build_dataset
from ssd.engine.inference import do_evaluation
from ssd.engine.trainer import do_train
from ssd.modeling.data_preprocessing import TrainAugmentation
from ssd.modeling.ssd import MatchPrior
from ssd.modeling.vgg_ssd import build_ssd_model
from ssd.module.prior_box import PriorBox
from ssd.utils import distributed_util
from ssd.utils.logger import setup_logger
from ssd.utils.lr_scheduler import WarmupMultiStepLR
from ssd.utils.misc import str2bool


def build_model(cfg, args):


    cfg.merge_from_file("configs/ssd512_voc0712.yaml")
    #cfg.merge_from_list(args.opts)
    cfg.freeze()
    # -----------------------------------------------------------------------------
    # Model
    # -----------------------------------------------------------------------------
    model = build_ssd_model(cfg)
    return model


# def main():
#     parser = argparse.ArgumentParser(description='Single Shot MultiBox Detector Training With PyTorch')
#     parser.add_argument(
#         "--config-file",
#         default="configs/ssd512_voc0712.yaml",
#         metavar="FILE",
#         help="path to config file",
#         type=str,
#     )
#     parser.add_argument("--local_rank", type=int, default=0)
#     parser.add_argument('--vgg', default='vgg16_reducedfc.pth',
#                         help='Pre-trained vgg model path, download from https://s3.amazonaws.com/amdegroot-models/vgg16_reducedfc.pth')
#     parser.add_argument('--resume', default='', type=str, help='Checkpoint state_dict file to resume training from')
#     parser.add_argument('--log_step', default=20, type=int, help='Print logs every log_step')
#     parser.add_argument('--save_step', default=1000, type=int, help='Save checkpoint every save_step')
#     parser.add_argument('--eval_step', default=1000, type=int,
#                         help='Evaluate dataset every eval_step, disabled when eval_step < 0')
#     parser.add_argument('--use_tensorboard', default=False, type=str2bool)
#     parser.add_argument(
#         "--skip-test",
#         dest="skip_test",
#         help="Do not test the final model",
#         action="store_true",
#     )
#     parser.add_argument(
#         "opts",
#         help="Modify config options using the command-line",
#         default=None,
#         nargs=argparse.REMAINDER,
#     )
#     args = parser.parse_args()
#     num_gpus = int(os.environ["WORLD_SIZE"]) if "WORLD_SIZE" in os.environ else 1
#     args.distributed = 0
#     args.num_gpus = num_gpus
#     print(num_gpus)
#     if torch.cuda.is_available():
#         # This flag allows you to enable the inbuilt cudnn auto-tuner to
#         # find the best algorithm to use for your hardware.
#
#         torch.backends.cudnn.benchmark = True
#     if args.distributed:
#         torch.cuda.set_device(args.local_rank)
#         torch.distributed.init_process_group(backend="nccl", init_method="env://")
#
#     logger = setup_logger("SSD", distributed_util.get_rank())
#     logger.info("Using {} GPUs".format(num_gpus))
#     logger.info(args)
#
#     cfg.merge_from_file(args.config_file)
#     cfg.merge_from_list(args.opts)
#     cfg.freeze()
#
#     logger.info("Loaded configuration file {}".format(args.config_file))
#     with open(args.config_file, "r") as cf:
#         config_str = "\n" + cf.read()
#         logger.info(config_str)
#     logger.info("Running with config:\n{}".format(cfg))
#
#     model = build_model(cfg, args)
#
#     if not args.skip_test:
#         logger.info('Start evaluating...')
#         torch.cuda.empty_cache()  # speed up evaluating after training finished
#         do_evaluation(cfg, model, cfg.OUTPUT_DIR, distributed=args.distributed)
#
#
# if __name__ == '__main__':
#     main()
