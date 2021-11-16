from transformers import BertForSequenceClassification, BertConfig, BertTokenizer
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
config = BertConfig.from_pretrained('bert-base-uncased')
config.num_labels = 8

model = BertForSequenceClassification.from_pretrained('topic_classification_model.bin', config=config)
print(model.device)

def predict(text):
  subwords = tokenizer.encode(text)
  subwords = torch.LongTensor(subwords).view(1, -1).to(model.device)

  logits = model(subwords)[0]
  label = torch.argmax(logits, dim=-1).item()
  return label

print(predict("I nearly died as my body burned itself from the inside out – after mistaking life-threatening disorder for i"))
print(predict("Hell ant’ found in 99 million year old amber"))