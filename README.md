# YouTube Analytics Dashboard

A comprehensive analytics dashboard built with Streamlit that provides detailed insights into YouTube channel performance. The dashboard visualizes key metrics, trends, and analytics using the YouTube Data API and Analytics API.

## 🌟 Features

### 📊 Interactive Dashboard
- **Channel Overview**
  - Total views counter
  - Subscriber count
  - Video count
  - Percentage change indicators

- **Video Performance Analytics**
  - Watch time metrics
  - View counts
  - Likes and comments tracking
  - Interactive bar charts
  - Detailed video-by-video analysis

- **Subscriber Growth Tracking**
  - Daily subscriber gains/losses
  - Interactive line graphs
  - Historical trend analysis

- **Performance Trends**
  - Moving averages
  - View count trends
  - Growth pattern analysis

- **Smart Insights**
  - Automated performance analysis
  - Data-driven recommendations
  - Trend identification

### ⚙️ Customization Options
- Adjustable date range (7-90 days)
- Multiple chart themes (Dark/Light/Presentation)
- Configurable metric displays
- Optional trend predictions

### 📥 Data Export
- Export video statistics
- Export subscriber data
- CSV format support

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-analytics-dashboard.git
cd youtube-analytics-dashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

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

## 📁 Project Structure
```
youtube-analytics/
├── config/
│   └── config.yaml         # API and database configuration
├── client_secrets.json     # Google API credentials
├── requirements.txt        # Python dependencies
├── main.py                # Streamlit dashboard
├── youtube_api.py         # YouTube API integration
├── database.py            # DataStax database handler
└── langflow_analyzer.py   # Analytics insights generator
```

## 🔧 Usage

1. Start the application:
```bash
streamlit run main.py
```

2. First-time setup:
   - Authenticate with your Google account
   - Grant required permissions
   - Wait for dashboard to load

3. Using the Dashboard:
   - Use sidebar to customize date range and appearance
   - Explore different metrics and charts
   - Export data as needed
   - View automated insights

## ⚙️ Configuration

Update `config/config.yaml` with your settings:
```yaml
youtube_api:
  scopes:
    - https://www.googleapis.com/auth/youtube.readonly
    - https://www.googleapis.com/auth/yt-analytics.readonly
    # ... other scopes

datastax:
  secure_connect_bundle: "path/to/bundle.zip"
  client_id: "your_client_id"
  client_secret: "your_client_secret"
```

## 📚 Dependencies

- Python 3.7+
- google-api-python-client
- google-auth-oauthlib
- streamlit
- pandas
- plotly
- cassandra-driver
- pyyaml

## 🔍 Troubleshooting

1. **API Authentication Issues**
   - Verify APIs are enabled in Google Cloud Console
   - Check `client_secrets.json` location
   - Ensure OAuth consent screen is configured

2. **No Data Displayed**
   - Confirm active YouTube channel
   - Verify channel has content
   - Check Google account permissions

3. **DataStax Connection Errors**
   - Verify credentials in config.yaml
   - Check secure connect bundle path
   - Application will run in view-only mode if connection fails

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [YouTube Data API](https://developers.google.com/youtube/v3)
- Uses [YouTube Analytics API](https://developers.google.com/youtube/analytics)
- Database integration with [DataStax Astra](https://astra.datastax.com/)
