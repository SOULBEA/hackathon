# filepath: src/datastax_connector.py
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

ASTRA_DB_BUNDLE_PATH = "C:\\Users\\Arpit Singh\\Downloads\\secure-connect-youtube-analytics.zip"  # Replace with the path to your secure connection bundle
ASTRA_DB_CLIENT_ID = "UjxZHsUkLjrPyzdeGnnicOiv"  # Replace with your Astra DB client ID
ASTRA_DB_CLIENT_SECRET = "H+ymN0pdHQ6tlS,CcNDnLo+l9OzC_1PwOdj+_fZNw.SYZjX.te2D+uLbB4UjZgNSx,9.x-eLw+XoxSYhq,vzA5nvIaDE2DLW+qpm3qReRzvpq7.JptxDCm8kl02C-pJQ"  # Replace with your Astra DB client secret
ASTRA_DB_KEYSPACE = "youtube"  # Replace with your Astra DB keyspace

def get_engagement_data(post_type):
    auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
    cluster = Cluster(cloud={'secure_connect_bundle': ASTRA_DB_BUNDLE_PATH}, auth_provider=auth_provider)
    session = cluster.connect(ASTRA_DB_KEYSPACE)
    query = f"SELECT * FROM engagement_data WHERE post_type='{post_type}'"
    rows = session.execute(query)
    return rows