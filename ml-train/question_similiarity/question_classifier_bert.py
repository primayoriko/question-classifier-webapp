# -*- coding: utf-8 -*-
"""Question_Classifier_BERT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y4qrplEI9IdBapJbaLD_fDjT5aaFZPrv

# Question Classifier using BERT
------
"""

!pip install -q kaggle
!pip install transformers==3.0.0

from google.colab import files

files.upload()

!mkdir ~/.kaggle

!cp kaggle.json ~/.kaggle/

!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets list

!kaggle competitions download -c quora-question-pairs --force

!unzip test.csv.zip
!unzip train.csv.zip

!wc -l train.csv

!head -n 10 train.csv

!wc -l test.csv

!head -n 10 test.csv

import os, sys, random
import itertools

import numpy as np
import pandas as pd

import torch
from torch import optim
import torch.nn.functional as F

from tqdm import tqdm

from transformers import BertForSequenceClassification, BertConfig, BertTokenizer

from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score

"""## Dataloader and utils function"""

from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    NUM_LABELS = 2
    
    def __init__(self, dataset_path, tokenizer, split, row_indexes=None):
        if (split == 'train' or split == 'dev'):
          df = pd.read_csv(dataset_path, sep=",")
          df['is_duplicate'] = pd.to_numeric(df['is_duplicate'], errors='ignore')
        else:
          df = pd.read_csv(dataset_path, sep=",")
          df['is_duplicate'] = 0

        if(row_indexes != None):
          df = df.iloc[row_indexes,:]
          df.reset_index(drop=True, inplace=True) 

        df['question1'] = df['question1'].str.lower()
        df['question2'] = df['question2'].str.lower()

        self.data = df
        self.tokenizer = tokenizer
    
    def __getitem__(self, index):
        data = self.data.loc[index,:]
        text1, text2, label = data['question1'], data['question2'], data['is_duplicate']
        subwords = self.tokenizer(text1, text2, padding='max_length', truncation=True, max_length=360)
        item = {key: torch.tensor(val) for key, val in subwords.items()}
        item['labels'] = torch.tensor(label)
        return item
    
    def __len__(self):
        return len(self.data)

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    
set_seed(42)

"""## Load model"""

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
config = BertConfig.from_pretrained('bert-base-uncased')
config.num_labels = CustomDataset.NUM_LABELS

model = BertForSequenceClassification.from_pretrained('bert-base-uncased', config=config)

"""## Load data"""

train_dataset_path = 'train.csv'
test_dataset_path = 'test.csv'

randomed_indexes = random.sample(range(0, 400000), 24000)

train_indexes = randomed_indexes[:20000]
dev_indexes = randomed_indexes[20000:]
test_indexes = random.sample(range(0, 100000), 4000)

train_dataset = CustomDataset(train_dataset_path, tokenizer, 'train', train_indexes)
dev_dataset = CustomDataset(train_dataset_path, tokenizer, 'dev', dev_indexes)
test_dataset = CustomDataset(test_dataset_path, tokenizer, 'test', test_indexes)

train_loader = DataLoader(dataset=train_dataset,  batch_size=16, shuffle=True)
dev_loader = DataLoader(dataset=dev_dataset,  batch_size=16, shuffle=False) 
test_loader = DataLoader(dataset=test_dataset,  batch_size=16,  shuffle=False)

print(train_dataset[0])
print(len(train_dataset))
print(len(dev_dataset))
print(len(test_dataset))

"""## Train"""

import torch, gc

gc.collect()
torch.cuda.empty_cache()

optimizer = optim.Adam(model.parameters(), lr=3e-5)
model = model.cuda()

device = 'cuda'
n_epochs = 4
for epoch in range(n_epochs):
    model.train()
    torch.set_grad_enabled(True)
 
    total_train_loss = 0
    list_hyp, list_label = [], []

    train_pbar = tqdm(train_loader, leave=True, total=len(train_loader))
    for i, batch in enumerate(train_pbar):
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs[0]
        loss.backward()
        optimizer.step()

        tr_loss = loss.item()
        total_train_loss = total_train_loss + tr_loss

        train_pbar.set_description("(Epoch {}) TRAIN LOSS:{:.4f}".format((epoch+1),
            total_train_loss/(i+1)))
        
    model.eval()
    torch.set_grad_enabled(False)
    
    total_loss, total_correct, total_labels = 0, 0, 0
    list_hyp, list_label = [], []

    pbar = tqdm(dev_loader, leave=True, total=len(dev_loader))
    for i, batch in enumerate(pbar):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs[0]

        valid_loss = loss.item()
        total_loss = total_loss + valid_loss

        pbar.set_description("DEV LOSS:{:.4f} ".format(total_loss/(i+1)))

        logits = outputs[1]
        batch_hyp = torch.argmax(logits, dim=-1)
        list_hyp += batch_hyp.cpu().numpy().tolist()
        list_label += labels.cpu().numpy().tolist()
    
    acc = accuracy_score(list_label, list_hyp)
    f1 = f1_score(list_label, list_hyp, average='macro')
    rec = recall_score(list_label, list_hyp, average='macro')
    prec = precision_score(list_label, list_hyp, average='macro')

    print(f"epoch: {epoch}")
    print("Acc: ", acc)
    print("F1: ", f1)
    print("recall: ", rec)
    print("precision: ", prec)

model.eval()
torch.save(model.state_dict(),'question_pair_model.bin')

"""## Evaluate on test"""

loaded_model = BertForSequenceClassification.from_pretrained('question_pair_model.bin', config=config)

# test_indexes = random.sample(range(0, 100000), 200)
# test_dataset = CustomDataset(test_dataset_path, tokenizer, 'test', test_indexes)
# test_loader = DataLoader(dataset=test_dataset,  batch_size=16,  shuffle=False)

model = loaded_model
model.eval()
torch.set_grad_enabled(False)
device = 'cpu'
total_loss, total_correct, total_labels = 0, 0, 0
list_hyp, list_label = [], []

pbar = tqdm(test_loader, leave=True, total=len(test_loader))
for i, batch in enumerate(pbar):
    input_ids = batch['input_ids'].to(device)
    attention_mask = batch['attention_mask'].to(device)
    labels = batch['labels'].to(device)
    outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
    loss = outputs[0]

    logits = outputs[1]
    batch_hyp = torch.argmax(logits, dim=-1)
    list_hyp += batch_hyp.cpu().numpy().tolist()
    list_label += labels.cpu().numpy().tolist()
    
print(list_label)
print(list_hyp)

df = pd.DataFrame({'label':list_hyp}).reset_index()
df.to_csv('qp_pred.csv', index=False)

print(df)

from transformers import BertForSequenceClassification, BertConfig, BertTokenizer
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
config = BertConfig.from_pretrained('bert-base-uncased')
config.num_labels = 2

model = BertForSequenceClassification.from_pretrained('question_pair_model.bin', config=config)
print(model.device)

def predict(text1, text2):
  subwords = tokenizer.encode(text1.lower(), text2.lower())
  subwords = torch.LongTensor(subwords).view(1, -1).to(model.device)

  logits = model(subwords)[0]
  label = torch.argmax(logits, dim=-1).item()
  return label

predict("when the sun rises?", "when the sun sets?")

predict("when benjamin franklin died?", "when adolf hitler died?")

predict("when i wake up today?", "when i brush my teeth today?")

predict("when i wake up today?", "when i sleep today?")