import streamlit as st
import preprocess
import re
import stats
import matplotlib.pyplot as plt
import numpy as np
import pickle

emotion = pickle.load(open('svc.pkl','rb'))

# emotion = pipeline("sentiment-analysis", model="arpanghoshal/EmoRoBERTa") 
# Use the pipeline


st.sidebar.title("Whatsapp Chat Analyzer")
st.sidebar.caption("The file you analysing won't be saved anywhere")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")

    df = preprocess.preprocess(data)

    user_list = df['User'].unique().tolist()

    if 'Group Notification' in user_list:
        user_list.remove('Group Notification')

    user_list.sort()

    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox(
        "Show analysis with respect to",user_list
    )

    st.title("Whatsapp App Chat Analysis for "+ selected_user)
    if st.sidebar.button("Show Analysis"):

        num_messages,num_words,media_omitted,links = stats.fetchstats(
            selected_user,df
        )

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            if num_words>0:
              st.title(num_messages)
            else:
                st.title(0)

        with col2:
            st.header("Total No. of Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(media_omitted)

        with col4:
            st.header("TotalLinks Shared")
            st.title(links)

        if selected_user == "Overall":

            st.title('Most Busy Users')
            busycount,newdf = stats.fetchbusyusers(df)
            fig,ax = plt.subplots()
            col1,col2 = st.columns(2)
            with col1:
                ax.bar(busycount.index,busycount.values,color='red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(newdf)
            
        st.title("Word Cloud")
        df_img = stats.createwordcloud(selected_user,df)
        if df_img!=False:
           fig,ax = plt.subplots()
           ax.imshow(df_img)
           st.pyplot(fig)


        most_common_df = stats.getcommonwords(selected_user,df)
        if most_common_df.shape[0]>0:
            fig,ax = plt.subplots()
            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks(rotation='vertical')
            st.title('Most common words')
            st.pyplot(fig)
        else:
            st.caption(f"We didn't find any words sent by {selected_user}")

        emoji_df = stats.getemojistats(selected_user,df)
        st.title("Emoji Analysis")
        if emoji_df.shape[0]>0:
          emoji_df.columns = ['Emoji','Count']
  
          
  
          col1,col2 = st.columns(2)
  
          with col1:
              st.dataframe(emoji_df)
  
          with col2:
            emojicount = list(emoji_df['Count'])
            perlist = [(i/sum(emojicount))*100 for i in emojicount]
            emoji_df['Percentage use'] = np.array(perlist)
            st.dataframe(emoji_df)
        else:
            st.caption(f"No emoji is sent by the {selected_user}")

        st.title("Monthly Timeline")
        if most_common_df.shape[0]>0:
             time = stats.monthtimeline(selected_user, df)
             fig, ax = plt.subplots()
             ax.plot(time['Time'], time['Message'], color='green')
             plt.xticks(rotation='vertical')
             plt.tight_layout()
             st.pyplot(fig)
        else:
            st.caption(f"We did not find any message from {selected_user}")

        # Activity maps

        st.title("Activity Maps")
        if most_common_df.shape[0]>0: 

          col1, col2 = st.columns(2)
  
          with col1:
  
              st.header("Most Busy Day")
  
              busy_day = stats.weekactivitymap(selected_user, df)
  
              fig, ax = plt.subplots()
              ax.bar(busy_day.index, busy_day.values, color='purple')
              plt.xticks(rotation='vertical')
              plt.tight_layout()
              st.pyplot(fig)
  
          with col2:

            st.header("Most Busy Month")
            busy_month = stats.monthactivitymap(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.caption(f"We did not find any message from {selected_user}")
        
        st.title("Text-Emotion Analysis")
        if most_common_df.shape[0]>0:
            num_len=len(most_common_df)
            sentence = ' '.join(most_common_df[0])
            result=emotion.predict([sentence])
            st.header(f"{result[0]}")
        else:
            st.caption(f"We did not find any message from {selected_user}")
