# Author: Naufa Prima Yoriko - 13518146

import os
import pickle
import re

import numpy as np
import tensorflow as tf

from string import punctuation

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from keras.preprocessing.sequence import pad_sequences


model_file_path = os.path.join(os.getcwd(), 'lstm_250_150_0.31_0.22_2.h5')
tokenizer_file_path = os.path.join(os.getcwd(), 'tokenizer.pickle')

model = tf.keras.models.load_model(model_file_path)

tokenizer = None
with open(tokenizer_file_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

def preprocess_text(text, lowercasing=True, remove_punctuation=False, remove_stopwords=False, stem_words=False):
    if lowercasing:
        text = text.lower()

    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\?", " ! ", text)
    text = re.sub(r"\.", " . ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\#", " # ", text)
    text = re.sub(r"\(", " ( ", text)
    text = re.sub(r"\)", " ) ", text)
    text = re.sub(r"\*", " * ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"e-mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    
    if remove_punctuation:
        text = "".join([c for c in text if c not in punctuation])
    
    if remove_stopwords:
        text = text.split()
        stop_words = set(stopwords.words('english'))
        text = [w for w in text if not w in stop_words]
        text = " ".join(text)
    
    if stem_words:
        text = text.split()
        stemmer = SnowballStemmer('english')
        stemmed_words = [stemmer.stem(word) for word in text]
        text = " ".join(stemmed_words)
    
    return text


def similiarity_predict(text1, text2):
    max_sequence_length = 64
    prep1, prep2 = [preprocess_text(text1)], [preprocess_text(text2)]

    tokenized1, tokenized2 = tokenizer.texts_to_sequences(prep1), tokenizer.texts_to_sequences(prep2)
    padded1, padded2 = pad_sequences(tokenized1, maxlen=max_sequence_length), pad_sequences(tokenized2, maxlen=max_sequence_length)

    res = model.predict([padded1, padded2], batch_size=8192, verbose=1)
    res += model.predict([padded2, padded1], batch_size=8192, verbose=1)
    res /= 2

    return res

if __name__ == '__main__':
    model.summary()
    print(f"{len(tokenizer.word_index)} unique tokens are found")
    # similiarity_predict("when the sun rises?", "when the sun sets?")
    # similiarity_predict("when benjamin franklin died?", "when adolf hitler died?")
    # similiarity_predict("when i wake up today?", "when i brush my teeth today?")
    # similiarity_predict("when i wake up today?", "when i sleep today?")
    similiarity_predict("how do you do?", "how do you do?")
    similiarity_predict("How can I be a good geologist?", "How can I be a great geologist?")
    # similiarity_predict("What causes a nightmare?","What causes nightmares that seem real?")
    similiarity_predict("How does the Surface Pro himself 4 compare with iPad Pro?", "Why did Microsoft choose core m3 and not core i3 home Surface Pro 4?")