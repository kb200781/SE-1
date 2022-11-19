# %%writefile app.py
import streamlit as st
import pandas as pd
import numpy as np
import re
import tweepy
# import altair as alt
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

st.title('Twitter Sentiment Analysis')
st.subheader('Get Tweets')

consumerKey = "we0Drpnvc1FZNazKkiKoFWlGf"
consumerSecret = "OXRvmJwM6ca9k90XMIMoktSCa5XvjNieqJivcfjbOAlmpO6RhH"
accessToken = "501682241-ZG1DshytyxUIUY8FXPoH2AXaDG9d5DQlORemfAzU"
accessTokenSecret = "mxwCYkDjgWG5qWy8ONtVs3j2lxiYSxyberVVa92jmd27z"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

def cleanTxt(text):
  text = re.sub('@[A-Za-z0-9]+', '', text) #Removed @mentions
  text = re.sub(r'#', '', text)            #Removing the # symbol
  text = re.sub(r'RT[\s]+', '', text)      #Removing RT
  text = re.sub(r"\S*https?:\S*", "", text) #Remove the hyperlink
  
  return text

def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
  return TextBlob(text).sentiment.polarity

def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'

keyword = st.text_input('Enter the keyword')

go = st.button('Get Tweets')

if go:

  tweets = tweepy.Cursor(api.search_tweets, tweet_mode = 'extended', q=keyword).items(100)

  tweet_list = []

  for tweet in tweets:
    tweet_list.append(tweet.text)
  
  df = pd.DataFrame(tweet_list)
  st.write(df)
