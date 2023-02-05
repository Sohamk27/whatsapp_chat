from urlextract import URLExtract
from wordcloud import WordCloud
import re
from collections import Counter
import pandas as pd
import emoji
import seaborn as sns


def fetch_stats(selected_user, df):
    if selected_user != 'Cumulative':
        df = df[df['user'] == selected_user]
    # 1 fetch number of msgs
    num_msg = df.shape[0]
    # 2 fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    # 3 fetch number of media
    count = 0
    for messages in df['message']:
        if messages == "<Media omitted>\n":
            count = count + 1
    # 4 fetch links
    links = []
    extractor = URLExtract()
    for messages in df['message']:
        links.extend(extractor.find_urls(messages))

    return num_msg, len(words), count, len(links)


def fetch_most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percentage'})
    return x, new_df


def create_word_cloud(selected_user, df):
    if selected_user != 'Cumulative':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def most_common_words(selected_user, df):
    if selected_user != 'Cumulative':
        df = df[df['user'] == selected_user]

    # remove group notifications
    temp = df[df['user'] != 'group_notification']
    # remove media omitted messages
    temp = temp[temp['message'] != '<Media omitted>\n']
    # remove stopwords
    f = open('hinglish_stopwords.txt', 'r', encoding='utf-8')
    stop_words = f.read()

    words = []

    for message in temp['message']:
        # remove emojis
        message = remove_emoji(message)
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)


    return pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user, df):
    if selected_user != 'Cumulative':
        df = df[df['user'] == selected_user]

    emojis_list = []
    for message in df['message']:
        emojis = emoji.distinct_emoji_list(message)
        emojis_list.extend([emoji.demojize(is_emoji) for is_emoji in emojis])
    emojis_list
    emoji_pic = []
    for emo in emojis_list:
        emoji_pic.append(emoji.emojize(emo))

    emoji_df = pd.DataFrame(Counter(emoji_pic).most_common(20))
    return emoji_df

def timeline_monthly(selected_user, df):
    if selected_user != 'Cumulative':
        df = df[df['user'] == selected_user]

    # df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def timeline_daily(selected_user, df):
    if selected_user != 'Cumulative':
        df = df[df['user'] == selected_user]

    # df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Cumulative':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Cumulative':
        df = df[df['user'] == selected_user]

    return df['month_name'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Cumulative':
        df = df[df['user'] == selected_user]

    activity_table = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_table