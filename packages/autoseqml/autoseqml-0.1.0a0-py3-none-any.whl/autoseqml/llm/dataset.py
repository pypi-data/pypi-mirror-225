import torch
from transformers import BertTokenizer
from torch.utils.data import Dataset

class Data(Dataset):
    def __init__(self, df, ds_model='bert', pretrained='bert-base-uncased'):
        if ds_model=='bert':
            tokenizer = BertTokenizer.from_pretrained(pretrained)
            self.x = [
                tokenizer(
                    code,
                    padding='max_length',
                    max_length=512,
                    truncation=True,
                    return_tensors='pt'
                ) for code in df['encode']
            ]
        elif ds_model=='gpt3':
            pass
        elif ds_model=='llama':
            pass
        
        label_dict = {k:v for v,k in enumerate(sorted(df['label'].unique().tolist()))}
        y = [label_dict[l] for l in df['label'].tolist()]
        self.y = torch.tensor(y)
        self.labels = len(label_dict)
    
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]
    
if __name__=='__main__':
    import pandas as pd
    df = pd.read_csv('../../data/train.csv')
    print(Data(df))
