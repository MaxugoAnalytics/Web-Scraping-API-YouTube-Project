
# YouTube Video Performance Analysis: Manchester United Focus

## Project Overview

This project involves analyzing YouTube video data, specifically focusing on content related to **Manchester United**. The primary objective is to uncover insights into video performance, audience engagement, and trends related to video duration, likes, comments, views, and upload patterns. 

The dataset was sourced using the **YouTube API** and **web scraping** techniques, focusing on YouTube channels that have garnered over **1 million views**. This analysis is designed to help content creators and marketers better understand the dynamics of successful YouTube channels, particularly those within the sports niche.

## Key Insights & Findings

### 1. **Correlation Between Views, Likes, and Comments**:
   - A **strong positive correlation** was found between **view_count** and **like_count** (0.90) as well as **view_count** and **comment_count** (0.82). This indicates that higher likes and comments often lead to more views, suggesting the importance of **audience engagement**.
   
### 2. **Video Duration and Engagement**:
   - **Video duration** showed weak correlations with views, likes, and comments:
     - Duration vs Views: 0.041
     - Duration vs Likes: -0.035
     - Duration vs Comments: -0.021
   - This suggests that **video length** does not have a significant impact on video performance, meaning creators can focus on content quality rather than worrying about the ideal video length.

### 3. **Optimal Times for Uploads**:
   - **Uploads** were most frequent on **Tuesday** and **Sunday**, with peak **views** occurring on **Monday** and **Saturday**.
   - **Upload months** with the highest frequency were **November** and **December**, while the most views occurred in **July** and **August**.
   - **Recommendation**: Posting on **Sundays and Tuesdays** aligns with the days with the most uploads, while **Monday and Saturday** are optimal for higher views, particularly in the **summer months**.

### 4. **Popular Keywords in Descriptions**:
   - A **word cloud** of video descriptions was generated to identify frequently used terms and themes that can drive engagement. This provides useful insights into keywords that attract more views.

## Project Structure

The project is divided into several sections:
1. **Data Collection**: Utilizing the YouTube API and web scraping to collect video data from channels discussing Manchester United.
2. **Data Cleaning & Preparation**: Preprocessing the data to ensure consistency and remove missing values.
3. **Exploratory Data Analysis (EDA)**: Analyzing the dataset to uncover insights through visualizations (correlation heatmap, scatter plots, and word cloud).
4. **Findings & Recommendations**: Based on the analysis, recommendations were made for content creators on optimizing video performance.

## Installation & Setup

### Requirements
- Python 3.x
- Required Libraries:
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `wordcloud`
  - `scikit-learn`
  - `statsmodels`
## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request. Contributions, issues, and suggestions are welcome!

## Contact

Maxwell Adigwe - [LinkedIn Profile](https://www.linkedin.com/in/maxwell-adigwe-7053a4312/)  
Email: maxwelladigwe1993@gmail.com

