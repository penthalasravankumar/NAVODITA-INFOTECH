import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Load data
intents = json.load(open("intents.json"))
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

def clean_up_sentence(sentence):
    tokens = nltk.word_tokenize(sentence)
    tokens = [lemmatizer.lemmatize(w.lower()) for w in tokens]
    return tokens

def bag_of_words(sentence, words):
    tokens = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in tokens:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return bag

def predict_class(sentence):
    bow = bag_of_words(sentence, words)
    scores = []
    for i, intent in enumerate(classes):
        score = np.dot(bow, bag_of_words(" ".join(intent.split()), words))  # naive similarity
        scores.append((intent, score))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores[0][0] if scores[0][1] > 0 else "no_match"

def get_response(tag):
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "I'm not sure I understand."

def chat():
    print("🤖 Chatbot is running! (type 'quit' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Chatbot: Bye!")
            break
        tag = predict_class(user_input)
        response = get_response(tag)
        print("Chatbot:", response)

if __name__ == "__main__":
    chat()
