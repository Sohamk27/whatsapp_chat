import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WHATSAPP CHAT ANALYZER")
user_list = []
with st.sidebar:
    uploaded_file = st.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df) # to show the dataframe
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Cumulative')
    with st.sidebar:
        selected_user = st.selectbox(
            'Show Analysis of User',
            user_list
        )
    if st.sidebar.button("Show Analysis"):
        num_msg, words, media, links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        st.title("Top Stats")

        with col1:
            st.write("Total Messages")
            st.text(num_msg)
        with col2:
            st.write("Total Words")
            st.text(words)
        with col3:
            st.write("Total Media")
            st.text(media)
        with col4:
            st.write("Total Links")
            st.text(links)


        # Monthly_Timeline
        monthly_timeline = helper.timeline_monthly(selected_user, df)
        st.title('Monthly Timeline')
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline['time'], monthly_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily Timeline
        daily_timeline = helper.timeline_daily(selected_user, df)
        st.title('Daily Timeline')
        fig, ax = plt.subplots()
        # plt.figure(figsize=(25, 10))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        #activity heat map
        st.title("weekly user activity")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest user in th group(Group Level)
        if selected_user == 'Cumulative':
            st.title('Most Busy Users')
            x, new_df = helper.fetch_most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df, width=400, height=350)

        # Wordcloud
        st.title('Word Cloud')
        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most Common WOrds
        most_common_df = helper.most_common_words(selected_user, df)
        st.title('Most Common Words')
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        # plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Analysis on Emojis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title('Emoji analysis')

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df, width=400, height=350)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1], labels=emoji_df[0], autopct="%0.2f")
            st.pyplot(fig)

