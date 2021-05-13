import argparse
import collections
import torch
import numpy as np
import data_loader.data_loaders as module_data
import model.loss as module_loss
import model.metric as model_metric
import model.model as module_arch
from parse_config import ConfiParser
from trainer import Trainer

#保证随机状态一致
SEED =123
torch.manual_seed(SEED)
torch.backends.cudnn.deterministic = True#为了提升计算速率
torch.backends.cudnn.benchmark = False#避免因为随机性产生差异
np.random.seed(SEED)

def main(config):
    logger = config.get_logger('train')

    #数据模块
    data_loader = config.init('data_loader',module_data)#通过config中的名字来指定
    valid_data_loader = data_loader.split_validation()

if __name__ == '__main__':
    args = argparse.ArgumentParser(description='PyTorch Templete')
    args.add_argument('-c','--config',default=None,type=str,
                      help='config file path (defaule:None)')
    args.add_argument('-r','--resume',default=None,type=str,
                      help='path to latest checkpoint (default:None)')
    args.add_argument('-d','--device',default=None,type=str,
                      help='indices of GPUs to enables (default:all)')

    #可以更改json文件中的参数直接用命令的方式
    CustomArgs = collections.namedtuple('CustomArgs','flags type target')
    options =[
        CustomArgs(['--lr', '--learning_rate'],type=float,target='optimizer;args;lr'),
        CustomArgs(['--bs','--batch-size'],type=int,target='data_loader;args;batch_size')
    ]
    config = CustomArgs.from_arg(args,options)
    main(config)