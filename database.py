from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import yaml

class DataStaxDB:
    def __init__(self):
        with open('config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.connect()

    def connect(self):
        cloud_config = {
            'secure_connect_bundle': self.config['datastax']['secure_connect_bundle']
        }
        
        auth_provider = PlainTextAuthProvider(
            self.config['datastax']['client_id'],
            self.config['datastax']['client_secret']
        )
        
        self.cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        self.session = self.cluster.connect()

    def save_analytics(self, channel_stats, video_stats, subscriber_stats):
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
        
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS youtube_analytics.video_stats (
                video_id text,
                date date,
                views bigint,
                likes bigint,
                comments bigint,
                PRIMARY KEY (video_id, date)
            )
        """)
        
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS youtube_analytics.subscriber_stats (
                date date PRIMARY KEY,
                gained int,
                lost int
            )
        """)
        
        # Insert data
        # Add your insert statements here based on the data format 