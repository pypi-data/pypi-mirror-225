import os
import random
# import wandb
import numpy as np
import pandas as pd

import torch
from torch.utils.data import DataLoader
from torchinfo import summary

import pytorch_lightning as pl
from pytorch_lightning.loggers import WandbLogger, TensorBoardLogger
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping

from .dataset import Data
from .classify import BertClassifier as bc

class LLM:
    """
    Large language model downstream tasks.
    """
    def __init__(self, data_dir='', mode='classify', seed=-1, pretrained='bert-base-uncased'):
        """
        :param data_dir: string, path for training files
        :param mode: string, downstream mode, must be one of 'classify' or 'forecast'
        :param seed: integer, random seed, -1 for totally random
        :param pretrained: string, pretrained model for downstream task
        """
        assert data_dir, 'please provide file path for training.'
        
        self.param = {}
        self.param['path']          = data_dir
        self.param['mode']          = mode
        self.param['pretrained']    = pretrained
        
        self.param['input_size']    = 768 if mode=='classify' else 1536
        self.param['hidden_size']   = 0
        self.param['output_size']   = 2
        self.param['hidden_layers'] = 0
        self.param['learning_rate'] = 1e-5
        self.param['dropout']       = 0.5
        self.param['batch_size']    = 16

        if seed>-1:
            torch.manual_seed(seed)
            np.random.seed(seed)
            random.seed(seed)
            pl.seed_everything(seed)
            
    def __setitem__(self, key, value):
        self.param[key] = value
        
    def __getitem__(self, key):
        return self.param.get(key, 'param not found')

    def split_data(self, val_split=0.8, test_split=0.9):
        data = [file for file in os.listdir(self.param['path']) if file[-3:]=='csv']
        if len(data)==1:
            df = pd.read_csv(os.path.join(self.param['path'],data[0]))
            train, val, test = np.split(df, [int(val_split*len(df)), int(test_split*len(df))])
        elif len(data)==2:
            df = pd.read_csv(os.path.join(self.param['path'],list(filter(lambda x:'train' in x, data))[0]))
            train, val = np.split(df, [int(val_split*len(df))])
            test = pd.read_csv(os.path.join(self.param['path'],list(filter(lambda x:'test' in x, data))[0]))
        elif len(data)==3:
            train = pd.read_csv(os.path.join(self.param['path'],list(filter(lambda x:'train' in x, data))[0]))
            val = pd.read_csv(os.path.join(self.param['path'],list(filter(lambda x:'val' in x, data))[0]))
            test = pd.read_csv(os.path.join(self.param['path'],list(filter(lambda x:'test' in x, data))[0]))
        else:
            return 'too many files for training'
        
        return train, val, test
        
    def train(self, train, val, prefix=''):
        if self.param['mode']=='classify':
#             wandb.init(project='test')
#             wandb.config.batch_size = self.param['batch_size']
            
            if prefix: self.prefix = prefix
            else: self.prefix = 'test'

            train = Data(train, pretrained=self.param['pretrained'])
            self.param['output_size'] = train.labels

            train = DataLoader(train, batch_size=self.param['batch_size'], shuffle=True, num_workers=4)
            val = DataLoader(
                Data(val, pretrained=self.param['pretrained']),
                batch_size=self.param['batch_size'], shuffle=False, num_workers=4
            )

            checkpoint_callback_val_loss = ModelCheckpoint(
                save_top_k=1,
                monitor="val_loss"
            )
            early_stop_callback = EarlyStopping(
                monitor='val_loss',  # Metric to monitor for improvement
                min_delta=0.0,       # Minimum change in the monitored metric to be considered as an improvement
                patience=5,          # Number of epochs with no improvement after which training will be stopped
                verbose=False,
                mode='min'           # Whether the monitored metric should be minimized or maximized
            )

            trainer = pl.Trainer(
                devices=1,
                accelerator='gpu',
                max_epochs=-1,
                precision=16,
                log_every_n_steps=10,
                check_val_every_n_epoch=1,
                callbacks=[checkpoint_callback_val_loss, early_stop_callback],
                logger=TensorBoardLogger("lightning_logs", name=self.prefix)
#                 logger=WandbLogger(project=self.prefix, log_model=True)
            )

            model = bc(
                input_size    = self.param['input_size'],
                hidden_size   = self.param['hidden_size'],
                output_size   = self.param['output_size'],
                hidden_layers = self.param['hidden_layers'],
                learning_rate = self.param['learning_rate'],
                dropout       = self.param['dropout'],
                pretrained    = self.param['pretrained']
            )

#             print(summary(model, [(1,512), (1,512)], dtypes=[torch.cuda.IntTensor, torch.cuda.IntTensor]))

            trainer.fit(model, train, val)
#             wandb.finish()
        
        elif self.param['mode']=='forecast':
            pass
    
    def test(self, test):
        test = DataLoader(Data(test, pretrained=self.param['pretrained']), batch_size=self.param['batch_size'], shuffle=False, num_workers=0)
        pass
    
    def save(self):
        pass
        

if __name__=='__main__':
    llm = LLM('../data')
    llm.split_data()

