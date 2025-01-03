# YouTube Channel Analytics Dashboard

A real-time analytics dashboard built with Streamlit that visualizes YouTube channel performance metrics using the YouTube Data API and Analytics API. The application provides insights into video performance, subscriber growth, and overall channel statistics.

## Features

- **Channel Overview Dashboard**
  - Total views count
  - Subscriber count 
  - Total videos count

- **Video Performance Analytics**
  - Watch time metrics
  - View counts
  - Likes and comments tracking
  - Interactive bar charts

- **Subscriber Growth Tracking**
  - Daily subscriber gains/losses
  - Interactive line graphs
  - Historical trend analysis

- **Data Storage**
  - Optional DataStax Astra DB integration
  - Persistent storage of analytics data
  - Historical data tracking

## Installation

1. Clone the repository:
git clone https://github.com/SOULBEA/hackathon.git


2. Install required packages:

pip install -r requirements.txt


3. Set up Google Cloud Project:
   - Create a project at [Google Cloud Console](https://console.cloud.google.com)
   - Enable YouTube Data API v3 and YouTube Analytics API
   - Create OAuth 2.0 credentials
   - Download credentials as `client_secrets.json`
   - Place `client_secrets.json` in project root directory

4. Configure DataStax (Optional):
   - Create account on [DataStax Astra](https://astra.datastax.com)
   - Download secure connect bundle
   - Update `config/config.yaml` with your credentials

## Project Structure
```filetree
youtube-analytics/
├── config/
│ └── config.yaml # API and database configuration
├── client_secrets.json # Google API credentials
├── requirements.txt # Python dependencies
├── main.py # Streamlit dashboard
├── youtube_api.py # YouTube API integration
└── database.py # DataStax database handler
```


## Usage

1. Start the application:

    ```bash
    streamlit run main.py
    ```


2. First-time setup:
   - Authenticate with your Google account
   - Grant required permissions
   - Wait for dashboard to load with your channel data

## Configuration

Update `config/config.yaml` with your settings


## Dependencies

- Python 3.7+
- google-api-python-client
- google-auth-oauthlib
- streamlit
- pandas
- plotly
- cassandra-driver
- pyyaml

## Troubleshooting

1. **API Authentication Issues**
   - Verify APIs are enabled in Google Cloud Console
   - Check `client_secrets.json` is in correct location
   - Ensure OAuth consent screen is configured
   - Add your email as test user if in testing mode

2. **No Data Displayed**
   - Confirm you have an active YouTube channel
   - Verify channel has content
   - Check you're using correct Google account

3. **DataStax Connection Errors**
   - Verify credentials in config.yaml
   - Check secure connect bundle path
   - Application will run in view-only mode if connection fails

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [YouTube Data API](https://developers.google.com/youtube/v3)
- Uses [YouTube Analytics API](https://developers.google.com/youtube/analytics)
- Database integration with [DataStax Astra](https://astra.datastax.com/)