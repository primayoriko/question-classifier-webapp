import os
import torch

from transformers import BertForSequenceClassification, BertConfig, BertTokenizer


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
config = BertConfig.from_pretrained('bert-base-uncased')
config.num_labels = 2

file_path = os.path.join(os.getcwd(), 'ml', 'question_pair_model.bin')
model = BertForSequenceClassification.from_pretrained(file_path, config=config)

def similiarity_predict(text1, text2):
    subwords = tokenizer.encode(text1.lower(), text2.lower())
    subwords = torch.LongTensor(subwords).view(1, -1).to(model.device)

    logits = model(subwords)[0]
    label = torch.argmax(logits, dim=-1).item()

    # print(label)
    return label == 1

if __name__ == '__main__':
    print(model.device)

    similiarity_predict("What causes a nightmare?","What causes nightmares that seem real?")
    similiarity_predict("when the sun rises dude?", "when the sun sets?")
    # similiarity_predict("when benjamin franklin died?", "when adolf hitler died?")
    # similiarity_predict("when i wake up today?", "when i brush my teeth today?")
    # similiarity_predict("when i wake up today?", "when i sleep today?")
    similiarity_predict("how do you do?", "how do you do")
    similiarity_predict("How can I be a good geologist?", "How can I be a great geologist?")
    similiarity_predict("What causes a nightmare?","What causes nightmares that seem real?")
    similiarity_predict("How does the Surface Pro himself 4 compare with iPad Pro?", "Why did Microsoft choose core m3 and not core i3 home Surface Pro 4?")
