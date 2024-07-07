from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji

extract = URLExtract()

def fetchstats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['User']==selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['Message']:
        words.extend(message.split())

    mediaomitted = df[df['Message']=='<Media omitted>']

    links =[]
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),mediaomitted.shape[0],len(links)

def fetchbusyusers(df):

    df = df[df['User']!='Group Notification']
    count=df['User'].value_counts().head()

    newdf = pd.DataFrame((df['User'].value_counts()/df.shape[0])*100)
    return count,newdf

def createwordcloud(selected_user,df):
    try:
        file = open('stop_hinglish.txt','r')
        stopwords = file.read().split("\n")
        file.close()
        
        if selected_user != "Overall":
            df = df[df['User'] == selected_user]
        
        if df.shape[0] > 0:
            wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white', stopwords=stopwords)
            df_wc = wc.generate(df['Message'].str.cat(sep=" "))
            return df_wc
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def getcommonwords(selected_user,df):

    file = open('stop_hinglish.txt','r')
    stopwords = file.read()
    stopwords = stopwords.split("\n")

    if selected_user!="Overall":
        df=df[df['User']==selected_user]

    temp = df[(df['User']!= "Group Notification")|(df['User']!= "<Media omitted>")]

    words=[]

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    mostcommon = pd.DataFrame(Counter(words).most_common(20))
    return mostcommon

def getemojistats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User']==selected_user]

    emojis=[]
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emojidf  = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojidf

def monthtimeline(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    temp = df.groupby(['Year', 'Month_num', 'Month']).count()[
        'Message'].reset_index()

    time = []
    for i in range(temp.shape[0]):
        time.append(temp['Month'][i]+"-"+str(temp['Year'][i]))

    temp['Time'] = time

    return temp


def monthactivitymap(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    return df['Month'].value_counts()


def weekactivitymap(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    return df['Day_name'].value_counts()