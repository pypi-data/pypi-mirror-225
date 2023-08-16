
from pytorch_lightning import LightningModule

import torch
from torch.optim import Adam, SGD
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
    def __init__(self, class_weights, learning_rate, variant, flavor, ratio, init_channels, r, ds_ver, augment_prob):
        super(classifier, self).__init__()
        self.save_hyperparameters()

        self.LR = learning_rate
        self.num_classes = 9
        self.augment_prob = augment_prob

        self.cm_total = []
        self.all_classes = []

        self.class_weights = torch.as_tensor(class_weights, device = torch.device("cuda"))

        def weights_init(m):
            if isinstance(m, Conv2d):
                kaiming_normal_(m.weight.data)

            elif isinstance(m, Linear):
                kaiming_normal_(m.weight.data)

            elif isinstance(m, BatchNorm2d) or isinstance(m, BatchNorm1d):
                ones_(m.bias.data)
                zeros_(m.bias.data)

        self.net = Resnet(
            variant = variant,
            flavor = flavor,
            ratio = ratio,
            init_channels = init_channels,
            r = r,
            ds_ver = ds_ver,
        )   

        self.net.apply(weights_init)

        self.net = self.net.to(memory_format = torch.channels_last)

        # ----------------------Metrics

        standard_metrics = MetricCollection([
            Accuracy(task = 'multiclass', num_classes = self.num_classes, average = 'macro'),
            Precision(task = 'multiclass', num_classes = self.num_classes, average = 'macro'),
            Recall(task = 'multiclass', num_classes = self.num_classes, average = 'macro'),
            F1Score(task = 'multiclass', num_classes = self.num_classes, average = 'macro'),
        ])

        weighted_metrics = MetricCollection([
            Accuracy(task = 'multiclass', num_classes = self.num_classes, average = 'weighted'),
            Precision(task = 'multiclass', num_classes = self.num_classes, average = 'weighted'),
            Recall(task = 'multiclass', num_classes = self.num_classes, average = 'weighted'),
            F1Score(task = 'multiclass', num_classes = self.num_classes, average = 'weighted'),
        ])

        self.std_metrics = standard_metrics
        self.wei_metrics = weighted_metrics

        self.train_step_output = []
        self.train_step_target = []

        self.valid_step_output = []
        self.valid_step_target = []

        self.test_step_output = []
        self.test_step_target = []

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
    
        x1, x2, y = batch
    
        pred_y = self((x1, x2))

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

        x1, x2, y = batch

        pred_y = self((x1, x2))

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
        
        x1, x2, y = batch

        pred_y = self((x1, x2))

        test_metric_1 = self.std_metrics.clone(prefix = 'test_', postfix = '_macro')
        test_metric_1 = self.wei_metrics.clone(prefix = 'test_', postfix = '_weighted')

        m1 = test_metric_1(pred_y, y)
        m2 = test_metric_1(pred_y, y)

        self.log_dict(m1, on_epoch = True, on_step = False, rank_zero_only = True)
        self.log_dict(m2, on_epoch = True, on_step = False, rank_zero_only = True)

    def configure_optimizers(self):

        n = 5

        optimizer = SGD(self.parameters(), lr = self.LR, weight_decay = 1E-2, nesterov = True) 
        scheduler = ReduceLROnPlateau(optimizer = optimizer, factor = (10 ** (0.5) / 10), cooldown = 0, patience = 5, min_lr = 1E-9)

        return {"optimizer": optimizer, "lr_scheduler": scheduler, "monitor": "valid_loss"}
    
    