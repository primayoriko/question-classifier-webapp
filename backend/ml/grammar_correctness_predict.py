import os
import torch

from transformers import BertForSequenceClassification, BertConfig, BertTokenizer


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
config = BertConfig.from_pretrained('bert-base-uncased')
config.num_labels = 2

file_path = os.path.join(os.getcwd(), 'ml', 'bert_cola.bin')
model = BertForSequenceClassification.from_pretrained(file_path, config=config)

def grammar_correctness_predict(text):
  subwords = tokenizer.encode(text)
  subwords = torch.LongTensor(subwords).view(1, -1).to(model.device)

  logits = model(subwords)[0]
  label = torch.argmax(logits, dim=-1).item()
  return label == 1

if __name__ == '__main__':
  print(model.device)
  print(grammar_correctness_predict("This is a text"))
  print(grammar_correctness_predict("This are a text"))