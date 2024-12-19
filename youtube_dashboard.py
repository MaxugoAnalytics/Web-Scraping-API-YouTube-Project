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
st.set_page_config(page_title="YouTube Video Performance Dashboard", layout="wide")

# Custom CSS for styling
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
        h1 {
            text-align: center;
            font-size: 2.5em;
            color: white;
            background-color: #FF0000;
            padding: 15px;
            border-radius: 10px;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }
        .kpi-container {
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            margin-top: 20px;
        }
        .kpi {
            border: 2px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            width: 22%;
            text-align: center;
            background-color: #007BFF;  /* Blue background */
            color: white;  /* White text */
        }
    </style>
""", unsafe_allow_html=True)

# Display YouTube logo on the top-right
st.markdown("""
    <div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 20px; margin-right: 20px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg" alt="YouTube Logo" width="150" />
    </div>
""", unsafe_allow_html=True)

# Dashboard Title below the logo with a blue background
st.markdown("""
    <h1 style="text-align: center; font-size: 1.8em; color: white; background-color: #007BFF; 
    padding: 15px; border-radius: 10px; margin-top: 10px;">
        YouTube Video Performance Dashboard by Maxwell Adigwe
    </h1>
""", unsafe_allow_html=True)



# Sidebar filter for channel name with 'All' option
channel_name = st.sidebar.selectbox("Select Channel", ["All"] + list(df['channelName'].unique()))
filtered_data = df if channel_name == "All" else df[df['channelName'] == channel_name]

# KPIs
total_views = filtered_data['viewCount'].sum()
total_likes = filtered_data['likeCount'].sum()
total_comments = filtered_data['commentCount'].sum()
total_videos = filtered_data.shape[0]

# Display KPIs
st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi">
            <strong>Total Views:</strong><br> {total_views:,}
        </div>
        <div class="kpi">
            <strong>Total Likes:</strong><br> {total_likes:,}
        </div>
        <div class="kpi">
            <strong>Total Comments:</strong><br> {total_comments:,}
        </div>
        <div class="kpi">
            <strong>Total Videos:</strong><br> {total_videos}
        </div>
    </div>
""", unsafe_allow_html=True)

# 3x3 Grid Layout
col1, col2, col3 = st.columns(3)

# Duration vs View Count
with col1:
    st.subheader("Duration vs View Count")
    fig1 = px.scatter(
        filtered_data, 
        x='durationSecs', 
        y='viewCount', 
        title="Duration vs View Count", 
        labels={"durationSecs": "Video Duration (seconds)", "viewCount": "View Count"}
    )
    st.plotly_chart(fig1)

# Correlation Heatmap
with col2:
    st.subheader("Correlation Heatmap")
    correlation = filtered_data[['viewCount', 'likeCount', 'commentCount', 'durationSecs']].corr()
    fig2 = px.imshow(correlation, text_auto=True, title="Correlation Heatmap")
    st.plotly_chart(fig2)

# Total Views by Month
with col3:
    st.subheader("Total Views by Month")
    monthly_views = filtered_data.groupby('month')['viewCount'].sum().reset_index()
    fig3 = px.bar(monthly_views, x='month', y='viewCount', title="Total Views by Month", labels={"month": "Month", "viewCount": "Total Views"})
    st.plotly_chart(fig3)

# Additional sections can follow the same structure as above



# Row 2: Visualizations
col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("Top 10 Most Viewed Videos")
    
    # Sorting by view count and selecting top 10
    top_10_videos = filtered_data.sort_values('viewCount', ascending=False).head(10)
    
    # Assuming 'description' contains titles or video names
    fig4 = px.bar(top_10_videos, x='description', y='viewCount', title="Top 10 Most Viewed Videos", labels={"description": "Video Description", "viewCount": "View Count"})
    fig4.update_xaxes(tickangle=45, tickmode='array')  # Rotate labels for better visibility
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
    st.subheader("Comments Distribution by Channel")
    fig9 = px.box(
        filtered_data,
        x='channelName',
        y='commentCount',
        title="Comments Distribution by Channel",
        labels={"channelName": "Channel Name", "commentCount": "Comment Count"},
        color='channelName',
    )
    st.plotly_chart(fig9)
