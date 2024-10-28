# lightning.py  
import torch 
import torch.nn as nn 
import torchvision 
import torchvision.transforms as transforms 
import matplotlib.pyplot as plt 

import pytorch_lightning as pl
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

# Hyper-parameters 
input_size = 784  # 28x28
hidden_size = 500 
num_classes = 10 
num_epochs = 2
batch_size = 100 
learning_rate = 0.001


class LitNeuralNet(pl.LightningModule):
    def __init__(self, input_size, hidden_size, num_classes):
        super(LitNeuralNet, self).__init__()
        self.validation_step_outputs = []
        self.input_size = input_size 
        self.l1 = nn.Linear(input_size, hidden_size) 
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(hidden_size, num_classes) 

    def forward(self, x):
        out = self.relu(self.l1(x))
        out = self.l2(out)
        # no activation and no softmax at the end 
        return out 
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=learning_rate) 
   
    def training_step(self, batch, batch_idx):
        images, labels = batch 
        images = images.reshape(-1, 28*28)

        # forward pass 
        outputs = self(images) 
        loss = F.cross_entropy(outputs, labels)
        tensorboard_logs = {'train_loss': loss} 
        return {'loss': loss, 'log': tensorboard_logs} 
    
    def train_dataloader(self):
        train_dataset = torchvision.datasets.MNIST(root='./data/', 
                         train=True, transform=transforms.ToTensor(), download=True)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, num_workers=4, shuffle=True) 
        return train_loader
    
    def validation_step(self, batch, batch_idx):
        images, labels = batch 
        images = images.reshape(-1, 28*28)

        # forward pass 
        outputs = self(images) 
        loss = F.cross_entropy(outputs, labels)
        self.validation_step_outputs.append(loss)
        tensorboard_logs = {'avg_val_loss': loss} 
        return {'val_loss': loss, 'log': tensorboard_logs} 
    
    def val_dataloader(self):
        val_dataset = torchvision.datasets.MNIST(root='./data/', 
                         train=False, transform=transforms.ToTensor(), download=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, num_workers=4, shuffle=False) 
        return val_loader    
    
    def on_validation_epoch_end(self):
        avg_loss = torch.stack(self.validation_step_outputs).mean()
        tensorboard_logs = {'avg_val_loss': avg_loss} 
        # self.validation_step_outputs.clear()  # free memory
        return {'val_loss': avg_loss, 'log': tensorboard_logs}
    

if __name__ == '__main__':
    trainer = pl.Trainer(max_epochs=num_epochs, fast_dev_run=False) 
    model = LitNeuralNet(input_size, hidden_size, num_classes) 
    trainer.fit(model) 