from google.oauth2.credentials import Credentials



from google_auth_oauthlib.flow import InstalledAppFlow



from googleapiclient.discovery import build



from googleapiclient.errors import HttpError



import yaml



import pandas as pd



from datetime import datetime, timedelta



import streamlit as st







class YouTubeAnalytics:



    def __init__(self):



        with open('config/config.yaml', 'r') as file:



            self.config = yaml.safe_load(file)



        



        self.youtube = None



        self.youtube_analytics = None



        self.authenticate()







    def authenticate(self):



        try:



            flow = InstalledAppFlow.from_client_secrets_file(



                'client_secrets.json',



                scopes=self.config['youtube_api']['scopes']



            )



            credentials = flow.run_local_server(port=8080)



            



            self.youtube = build('youtube', 'v3', credentials=credentials)



            self.youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)



        except Exception as e:



            st.error(f"Authentication Error: {str(e)}")



            raise







    def get_channel_stats(self):



        try:



            request = self.youtube.channels().list(



                part='statistics',



                mine=True



            )



            response = request.execute()



            return response['items'][0]['statistics']



        except HttpError as e:



            st.error(f"Error fetching channel stats: {str(e)}")



            return {



                'viewCount': 0,



                'subscriberCount': 0,



                'videoCount': 0



            }







    def get_video_performance(self, days=30):



        try:



            end_date = datetime.now().strftime('%Y-%m-%d')



            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')



            



            request = self.youtube_analytics.reports().query(



                ids='channel==MINE',



                startDate=start_date,



                endDate=end_date,



                metrics='estimatedMinutesWatched,views,likes,comments',



                dimensions='video',



                maxResults=20,



                sort='-views'



            )



            response = request.execute()



            



            if 'rows' in response:



                return pd.DataFrame(response['rows'], columns=['video_id', 'watch_time', 'views', 'likes', 'comments'])



            else:



                return pd.DataFrame(columns=['video_id', 'watch_time', 'views', 'likes', 'comments'])



        except HttpError as e:



            st.error(f"Error fetching video performance: {str(e)}")



            return pd.DataFrame(columns=['video_id', 'watch_time', 'views', 'likes', 'comments'])







    def get_subscriber_growth(self, days=30):



        try:



            end_date = datetime.now().strftime('%Y-%m-%d')



            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')



            



            request = self.youtube_analytics.reports().query(



                ids='channel==MINE',



                startDate=start_date,



                endDate=end_date,



                metrics='subscribersGained,subscribersLost',



                dimensions='day',



                sort='day'



            )



            response = request.execute()



            



            if 'rows' in response:



                return pd.DataFrame(response['rows'], columns=['date', 'gained', 'lost'])



            else:



                return pd.DataFrame(columns=['date', 'gained', 'lost'])



        except HttpError as e:



            st.error(f"Error fetching subscriber growth: {str(e)}")



            return pd.DataFrame(columns=['date', 'gained', 'lost']) 


