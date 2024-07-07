import streamlit as st
import numpy as np
import seaborn as sns
import pandas as pd
import re

def gettimedate(string):
    string = string.replace("\u2009", " ").replace("â€¯", "")
    string = string.split(',')
    date,time = string[0],string[1]
    time=time.split('-')
    time =time[0].strip()
    return date+" "+time

def getString(text):
    return text.split('\n')[0]

def check_date_format(date_str, date_format):
    try:
        # Try to parse the date string with the given format
        for i in range(len(date_str)):
           parsed_date = pd.to_datetime(date_str[i], format=date_format)
        return True
    except :
        # If parsing fails, return False
        return False
    

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4}\s*,?\s*\d{1,2}:\d{2}\s*(?:[aApP]\.?[mM]\.?)?\s*-\s*'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # return df
    df['message_date'] = df['message_date'].apply(lambda text: gettimedate(text))
    df.rename(columns={'message_date': 'Date'}, inplace=True)
    # return df

    users = []
    messages = []

    for message in df['user_message']:

        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])

        else:
            users.append('Group Notification')
            messages.append(entry[0])

    df['User'] = users
    df['message'] = messages

    # Apply additional string processing if needed
    df['Message'] = df['message'].apply(lambda text: getString(text))

    df = df.drop(['user_message'], axis=1)
    df = df[['Message', 'Date', 'User']]
    # return df

    # Convert the 'Date' column to datetime, handling errors by coercing invalid dates to NaT
    # df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows where 'Date' is NaT (if any)
    df = df.dropna(subset=['Date'])
    df['Date'] = df['Date'].apply(lambda x:x.replace('AM', 'am').replace('PM', 'pm'))
    # return df
    format='%d/%m/%y %I:%M %p'
    if check_date_format(df['Date'],format)==False:
        format='%d/%m/%Y %I:%M %p'
        if check_date_format(df['Date'],format)==False:
            format='%d/%m/%Y %H:%M'
            if check_date_format(df['Date'],format)==False:
                format='%d/%m/%y %H:%M'
                if check_date_format(df['Date'],format)==False:
                      format='%m/%d/%y %I:%M %p'

    # return df

    # Extract date components
    df['Only date'] = pd.to_datetime(df['Date'],format=format).dt.date

    df['Year'] = pd.to_datetime(df['Only date']).dt.year

    df['Month_num'] = pd.to_datetime(df['Only date']).dt.month

    df['Month'] = pd.to_datetime(df['Only date']).dt.month_name()

    df['Day'] = pd.to_datetime(df['Only date']).dt.day

    df['Day_name'] = pd.to_datetime(df['Only date']).dt.day_name()

    df['Hour'] = pd.to_datetime(df['Only date']).dt.hour

    df['Minute'] = pd.to_datetime(df['Only date']).dt.minute

    return df