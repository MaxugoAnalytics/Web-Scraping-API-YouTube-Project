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

# Ensure 'publishedAt' is a datetime object and extract day and month names
df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
df['day'] = df['publishedAt'].dt.day_name()  # Day name (e.g., Monday, Tuesday)
df['month'] = df['publishedAt'].dt.month_name()  # Month name (e.g., January, February)

# Row 1: Visualizations
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

# Row 2: Visualizations
col4, col5, col6 = st.columns(3)

# Top 10 Most Viewed Videos
with col4:
    st.subheader("Top 10 Most Viewed Videos")
    top_10_videos = filtered_data.sort_values('viewCount', ascending=False).head(10)
    fig4 = px.bar(top_10_videos, x='description', y='viewCount', title="Top 10 Most Viewed Videos", labels={"description": "Video Description", "viewCount": "View Count"})
    fig4.update_xaxes(tickangle=45)
    st.plotly_chart(fig4)

# Word Cloud for Video Descriptions
with col5:
    st.subheader("Word Cloud for Video Descriptions")
    wordcloud_filter = st.selectbox("Select Word Frequency Range", options=["All", "Top 10", "Top 20", "Top 50"], index=0)
    text = ' '.join(filtered_data['description'].dropna().head(int(wordcloud_filter.split()[-1])) if wordcloud_filter != "All" else filtered_data['description'].dropna())
    wordcloud = WordCloud(width=1000, height=700, background_color='white').generate(text)
    fig5 = px.imshow(wordcloud.to_array(), title="Word Cloud for Video Descriptions")
    fig5.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    st.plotly_chart(fig5)

# Likes vs Comments
with col6:
    st.subheader("Likes vs Comments")
    likes_comments_filter = st.selectbox("Select View Count Range for Likes vs Comments", options=["All", "0-10000", "10001-50000", "50001+"], index=0)
    filtered_data_likes_comments = filtered_data.query("viewCount <= 10000") if likes_comments_filter == "0-10000" else \
                                   filtered_data.query("10000 < viewCount <= 50000") if likes_comments_filter == "10001-50000" else \
                                   filtered_data.query("viewCount > 50000") if likes_comments_filter == "50001+" else \
                                   filtered_data
    fig6 = px.scatter(filtered_data_likes_comments, x='likeCount', y='commentCount', title="Likes vs Comments", labels={"likeCount": "Like Count", "commentCount": "Comment Count"})
    st.plotly_chart(fig6)

# Row 3: Visualizations
col7, col8, col9 = st.columns(3)

# Views vs Duration
with col7:
    st.subheader("Views vs Duration")
    duration_views_filter = st.selectbox("Select Duration Range for Views vs Duration", options=["All", "0-300", "301-600", "601-900", "901-1200", "1201+"], index=0)
    filtered_data_duration_views = filtered_data.query("durationSecs <= 300") if duration_views_filter == "0-300" else \
                                   filtered_data.query("300 < durationSecs <= 600") if duration_views_filter == "301-600" else \
                                   filtered_data.query("600 < durationSecs <= 900") if duration_views_filter == "601-900" else \
                                   filtered_data.query("900 < durationSecs <= 1200") if duration_views_filter == "901-1200" else \
                                   filtered_data.query("durationSecs > 1200") if duration_views_filter == "1201+" else \
                                   filtered_data
    fig7 = px.scatter(filtered_data_duration_views, x='durationSecs', y='viewCount', title="Views vs Duration", labels={"durationSecs": "Duration (seconds)", "viewCount": "View Count"})
    st.plotly_chart(fig7)

# Views vs Likes
with col8:
    st.subheader("Views vs Likes")
    views_likes_filter = st.selectbox("Select View Count Range for Views vs Likes", options=["All", "0-10000", "10001-50000", "50001+"], index=0)
    filtered_data_views_likes = filtered_data.query("viewCount <= 10000") if views_likes_filter == "0-10000" else \
                                filtered_data.query("10000 < viewCount <= 50000") if views_likes_filter == "10001-50000" else \
                                filtered_data.query("viewCount > 50000") if views_likes_filter == "50001+" else \
                                filtered_data
    fig8 = px.scatter(filtered_data_views_likes, x='viewCount', y='likeCount', title="Views vs Likes", labels={"viewCount": "View Count", "likeCount": "Like Count"})
    st.plotly_chart(fig8)

# Comments Distribution by Channel
with col9:
    st.subheader("Comments Distribution by Channel")
    fig9 = px.box(filtered_data, x='channelName', y='commentCount', title="Comments Distribution by Channel", labels={"channelName": "Channel Name", "commentCount": "Comment Count"}, color='channelName')
    st.plotly_chart(fig9)

# Row 4: Bar and Pie Charts
col10, col11 = st.columns(2)

# Bar Chart: Top Channels by Views
with col10:
    st.subheader("Top Channels by Total Views")
    top_channels = filtered_data.groupby("channelName")["viewCount"].sum().sort_values(ascending=False).head(10).reset_index()
    fig10 = px.bar(top_channels, x="channelName", y="viewCount", title="Top Channels by Total Views", labels={"channelName": "Channel Name", "viewCount": "Total Views"}, color="viewCount")
    fig10.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig10)

# Pie Chart: Video Count by Channel
with col11:
    st.subheader("Video Count Distribution by Channel")
    channel_counts = filtered_data['channelName'].value_counts().reset_index()
    channel_counts.columns = ['channelName', 'videoCount']
    fig11 = px.pie(channel_counts, values="videoCount", names="channelName", title="Video Count Distribution by Channel")
    st.plotly_chart(fig11)

# Row 5: Interactive Bar Chart and Histogram
col12, col13 = st.columns(2)

# Bar Chart: Most Commented Videos
with col12:
    st.subheader("Top 10 Most Commented Videos")
    most_commented_videos = filtered_data.sort_values("commentCount", ascending=False).head(10).reset_index()
    fig12 = px.bar(most_commented_videos, x="description", y="commentCount", title="Top 10 Most Commented Videos", labels={"description": "Video Description", "commentCount": "Comment Count"}, color="commentCount")
    fig12.update_xaxes(tickangle=45)
    st.plotly_chart(fig12)

# Histogram: Video Duration Distribution
with col13:
    st.subheader("Video Duration Distribution")
    fig13 = px.histogram(filtered_data, x="durationSecs", nbins=30, title="Video Duration Distribution", labels={"durationSecs": "Duration (Seconds)"})
    st.plotly_chart(fig13)

# Row 6: Additional Visualizations
col14, col15 = st.columns(2)

# Line Chart: Views, Likes, and Comments Over Time
with col14:
    st.subheader("Views, Likes, and Comments Over Time")
    time_series = filtered_data.groupby("day")[["viewCount", "likeCount", "commentCount"]].sum().reset_index()
    fig14 = px.line(time_series, x="day", y=["viewCount", "likeCount", "commentCount"], title="Views, Likes, and Comments Over Time", labels={"day": "Date", "value": "Count"}, color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96"])
    st.plotly_chart(fig14)

# Pie Chart: Audience Engagement Proportion
with col15:
    st.subheader("Audience Engagement Proportion")
    engagement_totals = {"Views": total_views, "Likes": total_likes, "Comments": total_comments}
    fig15 = px.pie(names=list(engagement_totals.keys()), values=list(engagement_totals.values()), title="Audience Engagement Proportion")
    st.plotly_chart(fig15)

# Row 7: Bar Chart and Box Plot
col16, col17 = st.columns(2)

# Bar Chart: Engagement Ratio by Channel
with col16:
    st.subheader("Engagement Ratio by Channel")
    filtered_data["engagement_ratio"] = (filtered_data["likeCount"] + filtered_data["commentCount"]) / filtered_data["viewCount"]
    channel_engagement = filtered_data.groupby("channelName")["engagement_ratio"].mean().sort_values(ascending=False).head(10).reset_index()
    fig16 = px.bar(channel_engagement, x="channelName", y="engagement_ratio", title="Engagement Ratio by Channel", labels={"channelName": "Channel Name", "engagement_ratio": "Engagement Ratio"}, color="engagement_ratio")
    fig16.update_xaxes(tickangle=45)
    st.plotly_chart(fig16)

# Box Plot: Distribution of Views per Video
with col17:
    st.subheader("Distribution of Views per Video")
    fig17 = px.box(filtered_data, y="viewCount", title="Distribution of Views per Video", labels={"viewCount": "View Count"}, color_discrete_sequence=["#FFA15A"])
    st.plotly_chart(fig17)

# Row 8: Monthly Video Uploads
col18, _ = st.columns([1, 0.1])

# Bar Chart: Monthly Video Uploads
with col18:
    st.subheader("Monthly Video Uploads")
    monthly_uploads = filtered_data.groupby("month")["description"].count().reset_index()
    monthly_uploads.columns = ["month", "videoCount"]
    fig18 = px.bar(monthly_uploads, x="month", y="videoCount", title="Monthly Video Uploads", labels={"month": "Month", "videoCount": "Video Count"})
    st.plotly_chart(fig18)
