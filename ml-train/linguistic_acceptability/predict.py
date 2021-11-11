from transformers import BertForSequenceClassification, BertConfig, BertTokenizer
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
config = BertConfig.from_pretrained('bert-base-uncased')
config.num_labels = 2

model = BertForSequenceClassification.from_pretrained('bert_cola.bin', config=config)
print(model.device)

def predict(text):
  subwords = tokenizer.encode(text)
  subwords = torch.LongTensor(subwords).view(1, -1).to(model.device)

  logits = model(subwords)[0]
  label = torch.argmax(logits, dim=-1).item()
  return label

print(predict("This is a text"))
print(predict("This are a text"))