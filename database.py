from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import yaml
import streamlit as st
from datetime import datetime

class DataStaxDB:
    def __init__(self):
        try:
            with open('config/config.yaml', 'r') as file:
                self.config = yaml.safe_load(file)
            
            # Verify configuration
            if not self.config['datastax']['secure_connect_bundle'] or \
               not self.config['datastax']['client_id'] or \
               not self.config['datastax']['client_secret']:
                raise ValueError("DataStax configuration is incomplete")
                
            self.connect()
        except Exception as e:
            st.warning(f"DataStax initialization failed: {str(e)}")
            raise

    def connect(self):
        try:
            cloud_config = {
                'secure_connect_bundle': self.config['datastax']['secure_connect_bundle']
            }
            
            auth_provider = PlainTextAuthProvider(
                self.config['datastax']['client_id'],
                self.config['datastax']['client_secret']
            )
            
            self.cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            self.session = self.cluster.connect()
            
        except Exception as e:
            st.error(f"Failed to connect to DataStax: {str(e)}")
            raise

    def save_analytics(self, channel_stats, video_stats, subscriber_stats):
        try:
            # Create keyspace if not exists
            self.session.execute("""
                CREATE KEYSPACE IF NOT EXISTS youtube_analytics
                WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
            """)
            
            # Create tables if not exists
            self.session.execute("""
                CREATE TABLE IF NOT EXISTS youtube_analytics.channel_stats (
                    date date PRIMARY KEY,
                    views bigint,
                    subscribers bigint,
                    videos int
                )
            """)
            
            # Insert current date's data
            current_date = datetime.now().date()
            self.session.execute("""
                INSERT INTO youtube_analytics.channel_stats (date, views, subscribers, videos)
                VALUES (%s, %s, %s, %s)
            """, (current_date, 
                  int(channel_stats['viewCount']),
                  int(channel_stats['subscriberCount']),
                  int(channel_stats['videoCount'])))
            
        except Exception as e:
            st.error(f"Failed to save analytics data: {str(e)}")
            raise 