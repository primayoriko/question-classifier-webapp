from transformers import BertForSequenceClassification, BertConfig, BertTokenizer
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
config = BertConfig.from_pretrained('bert-base-uncased')
config.num_labels = 2

model = BertForSequenceClassification.from_pretrained('question_pair_model.bin', config=config)

def predict(text1, text2):
    subwords = tokenizer.encode(text1.lower(), text2.lower())
    subwords = torch.LongTensor(subwords).view(1, -1).to(model.device)

    logits = model(subwords)[0]
    label = torch.argmax(logits, dim=-1).item()
    return label

if __name__ == '__main__':
    print(model.device)

    predict("when the sun rises?", "when the sun sets?")
    predict("when benjamin franklin died?", "when adolf hitler died?")
    predict("when i wake up today?", "when i brush my teeth today?")
    predict("when i wake up today?", "when i sleep today?")