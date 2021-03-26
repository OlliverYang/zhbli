# -*- coding: utf-8 -*-
import argparse
import os.path as osp
import sys
import numpy as np
import cv2
from loguru import logger
import random
import torch

from videoanalyst.config.config import cfg as root_cfg
from videoanalyst.config.config import specify_task
from videoanalyst.data import builder as dataloader_builder
from videoanalyst.engine import builder as engine_builder
from videoanalyst.model import builder as model_builder
from videoanalyst.optim import builder as optim_builder
from videoanalyst.utils import Timer, ensure_dir

seed = 31415926
# 排除PyTorch的随机性：
torch.manual_seed(seed)  # cpu种子
torch.cuda.manual_seed(seed)       # 为当前GPU设置随机种子
torch.cuda.manual_seed_all(seed)  # 所有可用GPU的种子

# 排除第三方库的随机性
np.random.seed(seed)
random.seed(seed)

# 排除cudnn加速的随机性：
torch.backends.cudnn.enabled = True   # 默认值
torch.backends.cudnn.benchmark = False  # 默认为False
torch.backends.cudnn.deterministic = True # 默认为False;benchmark为True时,y要排除随机性必须为True

cv2.setNumThreads(1)

# torch.backends.cudnn.enabled = False

# pytorch reproducibility
# https://pytorch.org/docs/stable/notes/randomness.html#cudnn
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True


def make_parser():
    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument('-cfg',
                        '--config',
                        default='',
                        type=str,
                        help='path to experiment configuration')
    parser.add_argument(
        '-r',
        '--resume',
        default="",
        help=r"completed epoch's number, latest or one model path")

    return parser


if __name__ == '__main__':
    # parsing
    parser = make_parser()
    parsed_args = parser.parse_args()
    # experiment config
    exp_cfg_path = osp.realpath(parsed_args.config)
    root_cfg.merge_from_file(exp_cfg_path)
    # resolve config
    root_cfg = root_cfg.train
    task, task_cfg = specify_task(root_cfg)
    task_cfg.freeze()
    # log config
    log_dir = osp.join(task_cfg.exp_save, task_cfg.exp_name, "logs")
    ensure_dir(log_dir)
    logger.configure(
        handlers=[
            dict(sink=sys.stderr, level="INFO"),
            dict(sink=osp.join(log_dir, "train_log.txt"),
                 enqueue=True,
                 serialize=True,
                 diagnose=True,
                 backtrace=True,
                 level="INFO")
        ],
        extra={"common_to_all": "default"},
    )
    # backup config
    # logger.info("Load experiment configuration at: %s" % exp_cfg_path)
    # logger.info(
    #    "Merged with root_cfg imported from videoanalyst.config.config.cfg")
    cfg_bak_file = osp.join(log_dir, "%s_bak.yaml" % task_cfg.exp_name)
    with open(cfg_bak_file, "w") as f:
        f.write(task_cfg.dump())
    # logger.info("Task configuration backed up at %s" % cfg_bak_file)
    # device config
    if task_cfg.device == "cuda":
        world_size = task_cfg.num_processes
        assert torch.cuda.is_available(), "please check your devices"
        assert torch.cuda.device_count(
        ) >= world_size, "cuda device {} is less than {}".format(
            torch.cuda.device_count(), world_size)
        devs = ["cuda:{}".format(i) for i in range(world_size)]
    else:
        devs = ["cpu"]

    # build model
    logger.info("build model")
    model = model_builder.build(task, task_cfg.model)

    DEBUG = False
    if not DEBUG:
        logger.info('move to GPU')
        model.set_device(devs[0])
    else:
        print('debug')

    # load data
    logger.info("load data")
    with Timer(name="Dataloader building", verbose=True):
        dataloader = dataloader_builder.build(task, task_cfg.data)

    # build optimizer
    logger.info("build optimizer")
    optimizer = optim_builder.build(task, task_cfg.optim, model)

    # build trainer
    logger.info("build trainer")
    trainer = engine_builder.build(task, task_cfg.trainer, "trainer", optimizer,
                                   dataloader)
    trainer.set_device(devs)
    trainer.resume(parsed_args.resume)
    # trainer.init_train()
    while not trainer.is_completed():
        trainer.train()
        trainer.save_snapshot()
    # export final model
    trainer.save_snapshot(model_param_only=True)
    logger.info("Training completed.")
