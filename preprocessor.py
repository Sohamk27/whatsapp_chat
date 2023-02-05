import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    message = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': message, 'date': date})
    # convert message date type to datetime
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %H:%M - ')

    # separate users from messages
    # df['user'] = df['message'].apply(lambda x: x.split(':')[0])
    # df['message'] = df['message'].apply(lambda x: ':'.join(x.split(':')[1:]))
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    df['month_name'] = df['date'].dt.month_name()
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if (hour == 23):
            period.append(str(hour) + " - " + str('00'))
        elif hour == 0:
            period.append(str('00') + " - " + str(hour + 1))
        else:
            period.append(str(hour) + " - " + str(hour + 1))
    df['period'] = period
    # df.drop(columns=['date'], inplace=True)
    return df

