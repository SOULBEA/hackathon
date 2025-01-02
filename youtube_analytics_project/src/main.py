# filepath: src/main.py
import streamlit as st
from youtube_analytics import get_channel_details
from datastax_connector import get_engagement_data
from langflow_analysis import analyze_engagement

st.title("YouTube Channel Analytics")

channel_id = st.text_input("Enter YouTube Channel ID")
if channel_id:
    channel_details = get_channel_details(channel_id)
    if channel_details:
        st.write("Channel Title:", channel_details["Title"])
        st.write("Subscribers:", channel_details["Subscribers"])
        st.write("Total Views:", channel_details["Total Views"])
        st.write("Total Videos:", channel_details["Total Videos"])
    else:
        st.write("Channel not found")

    post_types = ['carousel', 'reels', 'static']
    for post_type in post_types:
        data = get_engagement_data(post_type)
        insights = analyze_engagement(data)
        st.write(f"Insights for {post_type}: {insights}")