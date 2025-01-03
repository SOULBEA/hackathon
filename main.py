import streamlit as st



import plotly.express as px



import plotly.graph_objects as go



from youtube_api import YouTubeAnalytics



from database import DataStaxDB







def main():



    st.title("YouTube Channel Analytics")



    



    try:



        # Initialize YouTube API



        yt = YouTubeAnalytics()



        



        # Get analytics data



        channel_stats = yt.get_channel_stats()



        video_stats = yt.get_video_performance()



        subscriber_stats = yt.get_subscriber_growth()



        



        try:



            # Initialize DataStax and save data



            db = DataStaxDB()



            db.save_analytics(channel_stats, video_stats, subscriber_stats)



        except Exception as e:



            st.warning("DataStax connection failed. Running in view-only mode.")



            st.error(f"DataStax Error: {str(e)}")



        



        # Display channel overview



        st.header("Channel Overview")



        col1, col2, col3 = st.columns(3)



        



        with col1:



            st.metric("Total Views", channel_stats['viewCount'])



        with col2:



            st.metric("Subscribers", channel_stats['subscriberCount'])



        with col3:



            st.metric("Total Videos", channel_stats['videoCount'])



        



        # Video performance graph



        st.header("Video Performance")



        fig_videos = px.bar(



            video_stats,



            x='video_id',



            y=['watch_time', 'views', 'likes', 'comments'],



            title="Video Performance Metrics",



            barmode='group'



        )



        st.plotly_chart(fig_videos)



        



        # Subscriber growth graph



        st.header("Subscriber Growth")



        fig_subs = go.Figure()



        fig_subs.add_trace(go.Scatter(



            x=subscriber_stats['date'],



            y=subscriber_stats['gained'],



            name="Subscribers Gained",



            fill='tozeroy'



        ))



        fig_subs.add_trace(go.Scatter(



            x=subscriber_stats['date'],



            y=subscriber_stats['lost'],



            name="Subscribers Lost",



            fill='tozeroy'



        ))



        st.plotly_chart(fig_subs)



        



    except Exception as e:



        st.error(f"Application Error: {str(e)}")



        st.info("Please make sure you have enabled both YouTube Data API v3 and YouTube Analytics API in Google Cloud Console.")







if __name__ == "__main__":



    main() 


