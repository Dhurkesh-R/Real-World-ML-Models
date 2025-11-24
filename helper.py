import pandas as pd
from wordcloud import WordCloud
import re
import nltk
from collections import Counter
import emoji

def fetch_stats(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    num_messages = data.shape[0]
    words = data['message'].str.split().apply(len)
    num_words = words.sum()
    num_media_messages = data[data['message'] == '<Media omitted>\n'].shape[0]
    num_links = data['message'].str.contains('http').sum()

    return num_messages, num_words, num_media_messages, num_links

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user, df):
    f = open('tanglish_stopwords.txt','r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['message'] = df['message'].str.replace('<Media omitted>\n', '')
    df['message'] = df['message'].str.replace('http\S+|www\S+|https\S+', '', case=False)
    df['message'] = df['message'].str.replace('null', '')
    df['message'] = df['message'].str.replace('message', '')
    df['message'] = df['message'].str.replace('deleted', '')

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df['message'] = df['message'].apply(remove_stop_words)
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    f = open('tanglish_stopwords.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['message'] = df['message'].str.replace('<Media omitted>\n', '', regex=False)
    df['message'] = df['message'].str.replace('http\S+|www\S+|https\S+', '', case=False)
    df['message'] = df['message'].str.replace('null', '', regex=False)
    df['message'] = df['message'].str.replace('message', '', regex=False)
    df['message'] = df['message'].str.replace('deleted', '', regex=False)

    common_words = Counter()
    stopwords = set(nltk.corpus.stopwords.words('english'))

    for message in df['message']:
        message = re.sub(r'[^a-zA-Z\s]', '', message)
        message = re.sub(r'\s+', ' ', message).strip()
        words = message.split()
        for word in words:
            if word.lower() not in stopwords:
                if word.lower() not in stop_words:
                    common_words[word.lower()] += 1

    most_common_df = pd.DataFrame(common_words.most_common(20))
    return most_common_df

def most_common_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_counts = Counter(emojis)
    most_common_emojis_df = pd.DataFrame(emoji_counts.most_common(20))
    return most_common_emojis_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap