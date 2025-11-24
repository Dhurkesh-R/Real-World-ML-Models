import streamlit as st
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sklearn


tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

ps = PorterStemmer()
nltk.download('punkt')
nltk.download('stopwords')
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y=[]
    for i in text:
      if i.isalnum():
        y.append(i)

    text = y[:]
    y.clear()

    for i in text:
      if i not in stopwords.words('english') and i not in string.punctuation:
        y.append(i)

    text = y[:]
    y.clear()

    for i in text:
      y.append(ps.stem(i))

    return " ".join(y)

def predict(message):
  # preprocess the message
  transformed_message = transform_text(message)
  # vectorize the message
  vector_input = tfidf.transform([transformed_message])
  # predict
  result = model.predict(vector_input)[0]
  if result == 1:
      return "Spam"
  else:
      return "Not Spam"

st.title("Email/SMS Spam Classifier")

st.subheader("Enter the message below:")
message = st.text_area("Message")

# button to predict
if st.button("Predict"):
  st.header(predict(message))