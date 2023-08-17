
from pytorch_lightning import LightningModule

import torch
from torch.optim import Adam, SGD, AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.nn import functional as F

from torch.nn import Conv2d, Linear, BatchNorm2d, BatchNorm1d
from torch.nn.init import kaiming_normal_, ones_, zeros_

from torchmetrics import Accuracy, Precision, Recall, F1Score, ConfusionMatrix, MetricCollection, AUROC

from kornia.geometry.transform import rotate
import random

from argparse import ArgumentParser

#------------------------------
from .ResNet import Resnet
#------------------------------

torch.manual_seed(43)

class classifier(LightningModule):
    def __init__(self, trainer_args, optimizer_args, model_args):
        """

        trainer_args : (class_weights, augment_prob)

        optimizer_args : (learning_rate, weight_decay, momentum, optimizer)

        model_args : (variant, flavor, ratio, init_channels, radon_stack, downsample_version)

        """ 
        super(classifier, self).__init__()
        self.save_hyperparameters()
        
        class_weights, self.augment_prob = trainer_args
        self.optimizer_args = optimizer_args
        

        self.class_weights = torch.as_tensor(class_weights, device = torch.device("cuda"))

        def weights_init(m):
            if isinstance(m, Conv2d):
                kaiming_normal_(m.weight.data)

            elif isinstance(m, Linear):
                kaiming_normal_(m.weight.data)

            elif isinstance(m, BatchNorm2d) or isinstance(m, BatchNorm1d):
                ones_(m.bias.data)
                zeros_(m.bias.data)

        self.net = Resnet(model_args)

        self.net.apply(weights_init)

        self.net = self.net.to(memory_format = torch.channels_last)

        # ----------------------Metrics

        standard_metrics = MetricCollection([
            Accuracy(task = 'multiclass', num_classes = 9, average = 'macro'),
            Precision(task = 'multiclass', num_classes = 9, average = 'macro'),
            Recall(task = 'multiclass', num_classes = 9, average = 'macro'),
            F1Score(task = 'multiclass', num_classes = 9, average = 'macro'),
        ])

        weighted_metrics = MetricCollection([
            Accuracy(task = 'multiclass', num_classes = 9, average = 'weighted'),
            Precision(task = 'multiclass', num_classes = 9, average = 'weighted'),
            Recall(task = 'multiclass', num_classes = 9, average = 'weighted'),
            F1Score(task = 'multiclass', num_classes = 9, average = 'weighted'),
        ])

        self.train_step_output = []
        self.train_step_target = []

        self.valid_step_output = []
        self.valid_step_target = []

        self.test_step_output = []
        self.test_step_target = []

        self.std_metrics = standard_metrics
        self.wei_metrics = weighted_metrics

    def forward(self, x):

        x1, x2 = x

        rng = random.random()

        if rng < self.augment_prob:
            angle = random.choice(range(0, 180))

            angle_tensor =  torch.tensor(angle, dtype = torch.float32, device = torch.device("cuda"))

            x1 = rotate(x1, angle_tensor) / 127
            x2 = x2[:, :, :, (180-angle):(360-angle)]
        
        else:
            x1 = x1 / 127
            x2 = x2[:, :, :, 180:360]


        x1 = x1.to(memory_format = torch.channels_last)
        x2 = x2.to(memory_format = torch.channels_last)
        
        return self.net((x1, x2))

    def training_step(self, batch, batch_idx):
    
        x, y = batch
    
        pred_y = self(x)

        loss = F.cross_entropy(pred_y, y, weight = self.class_weights, label_smoothing = 0.05)

        self.train_step_output.extend(pred_y.argmax(dim=1).cpu().tolist())
        self.train_step_target.extend(y.cpu().tolist())

        self.log("train_loss", loss, on_epoch = True, on_step = False, rank_zero_only = True)

        return loss
    
    def on_train_epoch_end(self):

        train_output = torch.Tensor(self.train_step_output)
        train_target = torch.Tensor(self.train_step_target)

        train_metric_1 = self.std_metrics.clone(prefix = 'train_', postfix = '_macro').to('cpu')
        train_metric_2 = self.wei_metrics.clone(prefix = 'train_', postfix = '_weighted').to('cpu')

        m1 = train_metric_1(train_output, train_target)
        m2 = train_metric_2(train_output, train_target)

        self.log_dict(m1, on_epoch = True, on_step = False, rank_zero_only = True)
        self.log_dict(m2, on_epoch = True, on_step = False, rank_zero_only = True)

        self.train_step_output.clear()
        self.train_step_target.clear()
    
    def validation_step(self, batch, batch_idx):

        x, y = batch

        pred_y = self(x)

        loss = F.cross_entropy(pred_y, y, weight = self.class_weights, label_smoothing = 0.05)

        self.valid_step_output.extend(pred_y.argmax(dim=1).cpu().tolist())
        self.valid_step_target.extend(y.cpu().tolist())

        self.log("valid_loss", loss, on_epoch = True, on_step = False, rank_zero_only = True)

    def on_validation_epoch_end(self):

        valid_output = torch.Tensor(self.valid_step_output)
        valid_target = torch.Tensor(self.valid_step_target)

        valid_metric_1 = self.std_metrics.clone(prefix = 'valid_', postfix = '_macro').to('cpu')
        valid_metric_2 = self.wei_metrics.clone(prefix = 'valid_', postfix = '_weighted').to('cpu')

        m1 = valid_metric_1(valid_output, valid_target)
        m2 = valid_metric_2(valid_output, valid_target)

        self.log_dict(m1, on_epoch = True, on_step = False, rank_zero_only = True)
        self.log_dict(m2, on_epoch = True, on_step = False, rank_zero_only = True)

        self.valid_step_output.clear()
        self.valid_step_target.clear()


    def test_step(self, batch, batch_idx):
        
        x, y = batch

        pred_y = self(x)

        test_metric_1 = self.std_metrics.clone(prefix = 'test_', postfix = '_macro')
        test_metric_1 = self.wei_metrics.clone(prefix = 'test_', postfix = '_weighted')

        m1 = test_metric_1(pred_y, y)
        m2 = test_metric_1(pred_y, y)

        self.log_dict(m1, on_epoch = True, on_step = False, rank_zero_only = True)
        self.log_dict(m2, on_epoch = True, on_step = False, rank_zero_only = True)

    def configure_optimizers(self):

        lr, wd, m, opt = self.optimizer_args

        if opt == 'adam':
            optimizer = Adam(self.parameters(), lr = lr, weight_decay = wd, amsgrad = True) 
        elif opt == 'adamw':
            optimizer = AdamW(self.parameters(), lr = lr, weight_decay = wd, amsgrad = True) 
        elif opt == 'sgd':
            optimizer = SGD(self.parameters(), lr = lr, weight_decay = wd, momentum = m, nesterov = True) 

        scheduler = ReduceLROnPlateau(optimizer = optimizer, factor = (10 ** (0.5) / 10), cooldown = 0, patience = 5, min_lr = 1E-9)

        return {"optimizer": optimizer, "lr_scheduler": scheduler, "monitor": "valid_loss"}
    
    