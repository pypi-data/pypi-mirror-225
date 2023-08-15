# pretrained model
from transformers import BertModel

# torch package
import torch
from torch import nn
from torch.optim import AdamW

# torch ligntning
import pytorch_lightning as pl

class BertClassifier(pl.LightningModule):
    
    def __init__(
        self,
        input_size=768,
        hidden_size=0,
        output_size=2,
        hidden_layers=0,
        learning_rate=1e-5,
        dropout=0.5,
        pretrained='bert-base-uncased'
    ):
        super().__init__()
        print(f'input size: {input_size}, hidden layers: {hidden_layers}, hidden size: {hidden_size}, output size: {output_size}')
        print(f'Using pretrained model: {pretrained}')
        self.bert = BertModel.from_pretrained(pretrained)
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(input_size, output_size)
        self.fc_layers = nn.ModuleList()
        
        self.lr = learning_rate
        self.loss_fn = nn.CrossEntropyLoss()
        self.relu = nn.ReLU(inplace=True)
        
        if hidden_layers:
            for i in range(hidden_layers):
                in_size = hidden_size if i else input_size
                self.fc_layers.append(nn.Linear(in_size, hidden_size))
            self.fc_layers.append(nn.Linear(hidden_size, output_size))
        else:
            self.fc_layers.append(nn.Linear(input_size, output_size))
            
    def forward(self, ids, mask):
        _, x = self.bert(ids, mask, return_dict=False)
        x = self.dropout(x)
        for i,fc in enumerate(self.fc_layers):
#             if i==len(self.fc_layers)-1:
#                 x = fc(x)
#             else:
            x = fc(x)
            x = self.relu(x)
        return x
    
    def training_step(self, batch, batch_idx):
        ids, mask = batch[0]['input_ids'].squeeze(1), batch[0]['attention_mask']
        pred = self(ids, mask)
        loss = self.loss_fn(pred, batch[1])
        self.log('training loss', loss)
        
        acc = self.accuracy(pred, batch[1])
        self.log('train_acc', acc, on_epoch=True)
        return loss
    
    def validation_step(self, batch, batch_idx):
        ids, mask = batch[0]['input_ids'].squeeze(1), batch[0]['attention_mask']
        pred = self(ids, mask)
        loss = self.loss_fn(pred, batch[1])
        self.log('val_loss', loss)
        
        acc = self.accuracy(pred, batch[1])
        self.log('val_acc', acc, on_epoch=True)
    
    def test_step(self, batch, batch_idx):
        ids, mask = batch[0]['input_ids'].squeeze(1), batch[0]['attention_mask']
        pred = self(ids, mask)
        loss = self.loss_fn(pred, batch[1])
        self.log('test_loss', loss)
        
        acc = self.accuracy(pred, batch[1])
        self.log('test_acc', acc, on_epoch=True)
    
    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=self.lr, weight_decay=0.00001)

    def accuracy(self, pred, label):
        correct = (pred.argmax(dim=1)==label).sum().item()
        return correct/len(pred)

if __name__=='__main__':
    print('test')
