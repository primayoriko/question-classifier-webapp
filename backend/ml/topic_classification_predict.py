import os
import torch

from transformers import BertForSequenceClassification, BertConfig, BertTokenizer

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

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
config = BertConfig.from_pretrained('bert-base-uncased')
config.num_labels = 8


file_path = os.path.join(os.getcwd(), 'ml', 'topic_classification_model.bin')
model = BertForSequenceClassification.from_pretrained(file_path, config=config)

def topic_classification_predict(text):
  subwords = tokenizer.encode(text)
  subwords = torch.LongTensor(subwords).view(1, -1).to(model.device)

  logits = model(subwords)[0]
  label = torch.argmax(logits, dim=-1).item()
  return trans[label]

if __name__ == '__main__':
  print(model.device)
  print(topic_classification_predict("I nearly died as my body burned itself from the inside out – after mistaking life-threatening disorder for i"))
  print(topic_classification_predict("Hell ant’ found in 99 million year old amber"))