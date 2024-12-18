import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import gdown

# Download the dataset from Google Drive
file_id = '1dqqdQSmfeSyZTJmi89110AQeIHfERoq_'
url = f'https://drive.google.com/uc?export=download&id={file_id}'
output = 'data.csv'
gdown.download(url, output, quiet=False)

df = pd.read_csv(output)

# Custom CSS to make content full width
st.markdown("""
    <style>
        .main {
            max-width: 100%;
            padding: 0;
        }
        .block-container {
            padding-top: 0;
            padding-bottom: 0;
        }
        h1, h2, h3 {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown('<div class="top-right"><img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" width="50" height="50"></div>', unsafe_allow_html=True)

# Streamlit Title and Introduction
st.title("YouTube Video Performance Dashboard")
st.write("This dashboard provides insights into YouTube videos, including views, likes, comments, and more.")

# Sidebar filter for channel name with 'All' option
channel_name = st.sidebar.selectbox("Select Channel", ["All"] + list(df['channelName'].unique()))
if channel_name != "All":
    filtered_data = df[df['channelName'] == channel_name]
else:
    filtered_data = df  # Show all channels when "All" is selected

# Streamlit Header
st.subheader(f"Data for {channel_name if channel_name != 'All' else 'All Channels'}")

# KPI/Metrics
total_views = filtered_data['viewCount'].sum()
total_likes = filtered_data['likeCount'].sum()
total_comments = filtered_data['commentCount'].sum()
total_videos = filtered_data.shape[0]  # Total number of videos

# Display KPIs
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; font-size: 18px;">
        <div style="border: 2px solid #ccc; padding: 10px; border-radius: 5px; width: 22%; text-align: center;">
            <strong>Total Views:</strong><br> {total_views:,}
        </div>
        <div style="border: 2px solid #ccc; padding: 10px; border-radius: 5px; width: 22%; text-align: center;">
            <strong>Total Likes:</strong><br> {total_likes:,}
        </div>
        <div style="border: 2px solid #ccc; padding: 10px; border-radius: 5px; width: 22%; text-align: center;">
            <strong>Total Comments:</strong><br> {total_comments:,}
        </div>
        <div style="border: 2px solid #ccc; padding: 10px; border-radius: 5px; width: 22%; text-align: center;">
            <strong>Total Videos:</strong><br> {total_videos}
        </div>
    </div>
    """, unsafe_allow_html=True)


# 3x3 Grid Layout
col1, col2, col3 = st.columns(3)

# Row 1: Visualizations
with col1:
    st.subheader("Duration vs View Count")
    duration_filter = st.selectbox("Select Duration Range", options=["All", "0-300", "301-600", "601-900", "901-1200", "1201+"], index=0)
    if duration_filter == "All":
        filtered_data_duration = filtered_data
    elif duration_filter == "0-300":
        filtered_data_duration = filtered_data[filtered_data['durationSecs'] <= 300]
    elif duration_filter == "301-600":
        filtered_data_duration = filtered_data[(filtered_data['durationSecs'] > 300) & (filtered_data['durationSecs'] <= 600)]
    elif duration_filter == "601-900":
        filtered_data_duration = filtered_data[(filtered_data['durationSecs'] > 600) & (filtered_data['durationSecs'] <= 900)]
    elif duration_filter == "901-1200":
        filtered_data_duration = filtered_data[(filtered_data['durationSecs'] > 900) & (filtered_data['durationSecs'] <= 1200)]
    elif duration_filter == "1201+":
        filtered_data_duration = filtered_data[filtered_data['durationSecs'] > 1200]

    fig1 = px.scatter(filtered_data_duration, x='durationSecs', y='viewCount', title="Duration vs View Count", labels={"durationSecs": "Video Duration (seconds)", "viewCount": "View Count"})
    st.plotly_chart(fig1)

with col2:
    st.subheader("Correlation Heatmap")
    correlation_filter = st.selectbox("Select Correlation Metric", options=["All", "viewCount", "likeCount", "commentCount", "durationSecs"], index=0)

    if correlation_filter == "All":
        correlation_data = filtered_data[['viewCount', 'likeCount', 'commentCount', 'durationSecs']]
    else:
        correlation_data = filtered_data[[correlation_filter]]

    correlation = correlation_data.corr()
    fig2 = px.imshow(correlation, text_auto=True, title="Correlation Heatmap")
    st.plotly_chart(fig2)

with col3:
    st.subheader("Total Views by Month")
    month_filter = st.selectbox("Select Month Range", options=["All", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=0)

    if month_filter != "All":
        month_dict = {
            "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7,
            "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
        }
        filtered_data_month = filtered_data[filtered_data['month'] == month_dict[month_filter]]
    else:
        filtered_data_month = filtered_data

    monthly_views = filtered_data_month.groupby('month')['viewCount'].sum().reset_index()
    fig3 = px.bar(monthly_views, x='month', y='viewCount', title="Total Views by Month", labels={"month": "Month", "viewCount": "Total Views"})
    st.plotly_chart(fig3)

# Row 2: Visualizations
col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("Total Views by Day of the Week")
    day_filter = st.selectbox("Select Day", options=["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], index=0)

    if day_filter != "All":
        filtered_data_day = filtered_data[filtered_data['day'] == day_filter]
    else:
        filtered_data_day = filtered_data

    daily_views = filtered_data_day.groupby('day')['viewCount'].sum().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()
    fig4 = px.bar(daily_views, x='day', y='viewCount', title="Total Views by Day of the Week", labels={"day": "Day of the Week", "viewCount": "Total Views"})
    st.plotly_chart(fig4)

with col5:
    st.subheader("Word Cloud for Video Descriptions")
    wordcloud_filter = st.selectbox("Select Word Frequency Range", options=["All", "Top 10", "Top 20", "Top 50"], index=0)

    if wordcloud_filter == "Top 10":
        text = ' '.join(filtered_data['description'].dropna().head(10))
    elif wordcloud_filter == "Top 20":
        text = ' '.join(filtered_data['description'].dropna().head(20))
    elif wordcloud_filter == "Top 50":
        text = ' '.join(filtered_data['description'].dropna().head(50))
    else:
        text = ' '.join(filtered_data['description'].dropna())

    wordcloud = WordCloud(width=1000, height=700, background_color='white').generate(text)
    fig5 = px.imshow(wordcloud.to_array(), title="Word Cloud for Video Descriptions")
    fig5.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    st.plotly_chart(fig5)

with col6:
    st.subheader("Likes vs Comments")
    likes_comments_filter = st.selectbox("Select View Count Range for Likes vs Comments", options=["All", "0-10000", "10001-50000", "50001+"], index=0)

    if likes_comments_filter == "All":
        filtered_data_likes_comments = filtered_data
    elif likes_comments_filter == "0-10000":
        filtered_data_likes_comments = filtered_data[filtered_data['viewCount'] <= 10000]
    elif likes_comments_filter == "10001-50000":
        filtered_data_likes_comments = filtered_data[(filtered_data['viewCount'] > 10000) & (filtered_data['viewCount'] <= 50000)]
    elif likes_comments_filter == "50001+":
        filtered_data_likes_comments = filtered_data[filtered_data['viewCount'] > 50000]

    fig6 = px.scatter(filtered_data_likes_comments, x='likeCount', y='commentCount', title="Likes vs Comments", labels={"likeCount": "Like Count", "commentCount": "Comment Count"})
    st.plotly_chart(fig6)

# Row 3: Visualizations
col7, col8, col9 = st.columns(3)

with col7:
    st.subheader("Views vs Duration")
    duration_views_filter = st.selectbox("Select Duration Range for Views vs Duration", options=["All", "0-300", "301-600", "601-900", "901-1200", "1201+"], index=0)

    if duration_views_filter == "All":
        filtered_data_duration_views = filtered_data
    elif duration_views_filter == "0-300":
        filtered_data_duration_views = filtered_data[filtered_data['durationSecs'] <= 300]
    elif duration_views_filter == "301-600":
        filtered_data_duration_views = filtered_data[(filtered_data['durationSecs'] > 300) & (filtered_data['durationSecs'] <= 600)]
    elif duration_views_filter == "601-900":
        filtered_data_duration_views = filtered_data[(filtered_data['durationSecs'] > 600) & (filtered_data['durationSecs'] <= 900)]
    elif duration_views_filter == "901-1200":
        filtered_data_duration_views = filtered_data[(filtered_data['durationSecs'] > 900) & (filtered_data['durationSecs'] <= 1200)]
    elif duration_views_filter == "1201+":
        filtered_data_duration_views = filtered_data[filtered_data['durationSecs'] > 1200]

    fig7 = px.scatter(filtered_data_duration_views, x='durationSecs', y='viewCount', title="Views vs Duration", labels={"durationSecs": "Duration (seconds)", "viewCount": "View Count"})
    st.plotly_chart(fig7)

with col8:
    st.subheader("Views vs Likes")
    views_likes_filter = st.selectbox("Select View Count Range for Views vs Likes", options=["All", "0-10000", "10001-50000", "50001+"], index=0)

    if views_likes_filter == "All":
        filtered_data_views_likes = filtered_data
    elif views_likes_filter == "0-10000":
        filtered_data_views_likes = filtered_data[filtered_data['viewCount'] <= 10000]
    elif views_likes_filter == "10001-50000":
        filtered_data_views_likes = filtered_data[(filtered_data['viewCount'] > 10000) & (filtered_data['viewCount'] <= 50000)]
    elif views_likes_filter == "50001+":
        filtered_data_views_likes = filtered_data[filtered_data['viewCount'] > 50000]

    fig8 = px.scatter(filtered_data_views_likes, x='viewCount', y='likeCount', title="Views vs Likes", labels={"viewCount": "View Count", "likeCount": "Like Count"})
    st.plotly_chart(fig8)

with col9:
    # Placeholder for future visualizations or metrics
    st.write("Future Visualization Placeholder")
