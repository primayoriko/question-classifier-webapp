# -*- coding: utf-8 -*-
"""[Tubes NLP] Topic Classfication

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17HL6LSN2CdEGNDckzJhiK0bBuXTkQZsS
"""
import os, sys, random
import itertools

import numpy as np
import pandas as pd

import torch
from torch import optim
import torch.nn.functional as F

from tqdm import tqdm

from transformers import BertForSequenceClassification, BertConfig, BertTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score

from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    NUM_LABELS = 8
    
    def __init__(self, dataset_path, tokenizer, split,row_indexes=None):
        if (split=='train' or split=='dev'):
          df = pd.read_csv(dataset_path,sep=";")
          df['label'] = df['topic'].factorize()[0]
          label_id_df = df[['topic', 'label']].drop_duplicates().sort_values('label')
          label_to_id = dict(label_id_df.values)
          id_to_label = dict(label_id_df[['label', 'topic']].values)
        else:
          df = pd.read_csv(dataset_path, sep=";")
          df['label'] = 0
        if(row_indexes != None):
          df = df.iloc[row_indexes,:]
          df.reset_index(drop=True, inplace=True) 
        df['title'] = df['title'].str.lower()

        
        self.data = df
        self.tokenizer = tokenizer
    
    def __getitem__(self, index):
        data = self.data.loc[index,:]
        text, label = data['title'], data['label']
        subwords = self.tokenizer(text, padding='max_length', truncation=True, max_length=360)
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

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
config = BertConfig.from_pretrained('bert-base-uncased')
config.num_labels = CustomDataset.NUM_LABELS

model = BertForSequenceClassification.from_pretrained('bert-base-uncased', config=config)

train_dataset_path = '/content/train.csv'
dev_dataset_path = '/content/labelled_newscatcher_dataset.csv'

train_dataset = CustomDataset(train_dataset_path, tokenizer, "train")
dev_dataset = CustomDataset(dev_dataset_path, tokenizer, "dev")

train_loader = DataLoader(dataset=train_dataset,  batch_size=8, shuffle=True) 
dev_loader = DataLoader(dataset=dev_dataset,  batch_size=8, shuffle=False)

randomed_indexes = random.sample(range(0, 100000), 10000)
train_indexes = randomed_indexes[:20000]
dev_indexes = randomed_indexes[5000:]
test_indexes = random.sample(range(0, 25000), 2000)

train_dataset_path = '/content/train.csv'
dev_dataset_path = '/content/labelled_newscatcher_dataset.csv'
print(train_indexes)
print(dev_indexes)
train_dataset = CustomDataset(train_dataset_path, tokenizer, "train",train_indexes)
dev_dataset = CustomDataset(dev_dataset_path, tokenizer, "dev",dev_indexes)

train_loader = DataLoader(dataset=train_dataset,  batch_size=8, shuffle=True) 
dev_loader = DataLoader(dataset=dev_dataset,  batch_size=8, shuffle=False)

print(train_dataset[0])
print(len(train_dataset))
print(len(dev_dataset))

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,6))
train_dataset.data.groupby('topic').title.count().plot.bar(ylim=0)
plt.show()

optimizer = optim.Adam(model.parameters(), lr=3e-5)
model = model.cuda()

# Train
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
        
    # # eval on dev
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
torch.save(model.state_dict(),'topic_classification_model.bin')

loaded_model = BertForSequenceClassification.from_pretrained('/content/topic_classification_model.bin', config=config)

test_dataset = CustomDataset(dev_dataset_path, tokenizer, "test",test_indexes)
test_loader = DataLoader(dataset=test_dataset,  batch_size=8, shuffle=False)
print(test_dataset[0])
print(len(test_dataset))

model= loaded_model
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
df.to_csv('pred_tc.csv', index=False)

print(df)

trans = {
    0:'SCIENCE',
    1:'TECHNOLOGY',
    2:'HEALTH',
    3:'WORLD',
    4:'ENTERTAINMENT',
    5:'SPORTS',
    6:'BUSINESS',
    7:'NATION'
}
def predict(text):
  subwords = tokenizer.encode(text)
  subwords = torch.LongTensor(subwords).view(1, -1).to(model.device)

  logits = model(subwords)[0]
  label = torch.argmax(logits, dim=-1).item()
  return trans[label]

predict("A closer look at water-splitting's solar fuel potential")

predict("Come See What It’s Like To Play Microsoft Flight Simulator")

predict("I nearly died as my body burned itself from the inside out – after mistaking life-threatening disorder for i")

predict("Hell ant’ found in 99 million year old amber")