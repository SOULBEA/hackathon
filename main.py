import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from youtube_api import YouTubeAnalytics
from database import DataStaxDB
from langflow_analyzer import AnalyticsInsightGenerator

# Set page configuration
st.set_page_config(
    page_title="YouTube Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #0E1117;
    }
    
    /* Headers */
    h1 {
        color: #FF4B4B;
        font-size: 2.5rem !important;
        font-weight: 700;
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(90deg, #FF4B4B 0%, #FF9B9B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h2 {
        color: #FFFFFF;
        font-size: 1.8rem !important;
        padding-top: 1rem;
        padding-bottom: 0.5rem;
    }
    
    /* Metric containers */
    .metric-container {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #FF4B4B;
    }
    
    /* Charts */
    .chart-container {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Insights */
    .insights-header {
        color: #FF4B4B;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0;
    }
    
    .insight-box {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #FF4B4B;
        transition: transform 0.2s;
    }
    
    .insight-box:hover {
        transform: translateX(10px);
    }
    
    /* Metrics */
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #FF4B4B;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #FFFFFF;
        opacity: 0.8;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .stPlotlyChart {
        animation: fadeIn 1s ease-in;
    }
    
    /* Chat container */
    .chat-container {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .user-message {
        background-color: #2E2E2E;
        border-radius: 10px;
        padding: 10px 15px;
        margin: 5px 0;
        margin-left: 20%;
        margin-right: 5px;
        color: #FFFFFF;
    }
    
    .bot-message {
        background-color: #FF4B4B22;
        border-radius: 10px;
        padding: 10px 15px;
        margin: 5px 0;
        margin-right: 20%;
        margin-left: 5px;
        color: #FFFFFF;
        border-left: 4px solid #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ Dashboard Settings")
    
    # Date range selection
    st.subheader("Date Range")
    days = st.slider("Days of data to show", 7, 90, 30)
    
    # Chart customization
    st.subheader("Chart Settings")
    chart_theme = st.selectbox(
        "Chart Theme",
        ["dark", "light", "presentation"],
        index=0
    )
    
    # Metric display options
    st.subheader("Metrics")
    show_percentages = st.checkbox("Show % changes", value=True)
    show_predictions = st.checkbox("Show trend predictions", value=False)

def get_chart_theme():
    if chart_theme == "light":
        return {
            "template": "plotly_white",
            "plot_bgcolor": 'rgba(255,255,255,0)',
            "paper_bgcolor": 'rgba(255,255,255,0)',
            "font_color": "#333333"
        }
    elif chart_theme == "presentation":
        return {
            "template": "plotly",
            "plot_bgcolor": 'rgba(0,0,0,0)',
            "paper_bgcolor": 'rgba(0,0,0,0.05)',
            "font_color": "#FFFFFF"
        }
    else:  # dark theme
        return {
            "template": "plotly_dark",
            "plot_bgcolor": 'rgba(0,0,0,0)',
            "paper_bgcolor": 'rgba(0,0,0,0)',
            "font_color": "#FFFFFF"
        }

def main():
    # Header with logo
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("📊 YouTube Analytics Dashboard")
    
    try:
        # Initialize YouTube API only once
        if 'yt' not in st.session_state:
            st.session_state.yt = YouTubeAnalytics()
            
        # Use the stored instance
        yt = st.session_state.yt
        
        # Get analytics data
        if 'channel_stats' not in st.session_state or st.session_state.get('current_days') != days:
            st.session_state.channel_stats = yt.get_channel_stats()
            st.session_state.video_stats = yt.get_video_performance(days=days)
            st.session_state.subscriber_stats = yt.get_subscriber_growth(days=days)
            st.session_state.current_days = days
        
        channel_stats = st.session_state.channel_stats
        video_stats = st.session_state.video_stats
        subscriber_stats = st.session_state.subscriber_stats

        # Channel Overview with animated counters
        st.markdown("<h2>📈 Channel Overview</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        metrics = [
            {"label": "Total Views", "value": channel_stats['viewCount'], "icon": "👁️"},
            {"label": "Subscribers", "value": channel_stats['subscriberCount'], "icon": "🎯"},
            {"label": "Total Videos", "value": channel_stats['videoCount'], "icon": "🎬"}
        ]
        
        if show_percentages:
            for col, metric in zip([col1, col2, col3], metrics):
                with col:
                    current_value = int(metric['value'])
                    if 'previous_' + metric['label'] in st.session_state:
                        previous_value = st.session_state['previous_' + metric['label']]
                        if previous_value > 0:
                            change = ((current_value - previous_value) / previous_value) * 100
                            delta_color = "normal" if change >= 0 else "inverse"
                            st.metric(
                                metric['label'],
                                f"{metric['icon']} {current_value:,}",
                                f"{change:+.1f}%",
                                delta_color=delta_color
                            )
                        else:
                            st.metric(metric['label'], f"{metric['icon']} {current_value:,}")
                    else:
                        st.metric(metric['label'], f"{metric['icon']} {current_value:,}")
                    st.session_state['previous_' + metric['label']] = current_value
        
        # Video Performance
        st.markdown("<h2>🎥 Video Performance</h2>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_videos = px.bar(
                video_stats,
                x='video_id',
                y=['watch_time', 'views', 'likes', 'comments'],
                title="Video Metrics Comparison",
                barmode='group'
            )
            
            theme = get_chart_theme()
            fig_videos.update_layout(**theme, hovermode='x')
            st.plotly_chart(fig_videos, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("🎥 Detailed Video Analysis"):
            try:
                if not video_stats.empty and len(video_stats) > 0:
                    selected_video = st.selectbox(
                        "Select a video to analyze:",
                        options=video_stats['video_id'].tolist(),
                        format_func=lambda x: f"Video {x[:8]}..."
                    )
                    
                    if selected_video in video_stats['video_id'].values:
                        video_data = video_stats[video_stats['video_id'] == selected_video].iloc[0]
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Views", f"{int(video_data['views']):,}")
                        with col2:
                            st.metric("Watch Time", f"{int(video_data['watch_time']):,} mins")
                        with col3:
                            st.metric("Likes", f"{int(video_data['likes']):,}")
                        with col4:
                            st.metric("Comments", f"{int(video_data['comments']):,}")
                else:
                    st.info("No video data available for the selected time period.")
            except Exception as e:
                st.error(f"Error displaying video analysis: {str(e)}")
        
        # Subscriber Growth
        st.markdown("<h2>👥 Subscriber Growth</h2>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_subs = go.Figure()
            
            fig_subs.add_trace(go.Scatter(
                x=subscriber_stats['date'],
                y=subscriber_stats['gained'],
                name="Subscribers Gained",
                fill='tozeroy',
                line=dict(color='#FF4B4B')
            ))
            
            fig_subs.add_trace(go.Scatter(
                x=subscriber_stats['date'],
                y=subscriber_stats['lost'],
                name="Subscribers Lost",
                fill='tozeroy',
                line=dict(color='#FF9B9B')
            ))
            
            fig_subs.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x'
            )
            st.plotly_chart(fig_subs, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Performance Trends
        st.markdown("<h2>📊 Performance Trends</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            # Calculate moving averages
            if not video_stats.empty:
                video_stats['ma_views'] = video_stats['views'].rolling(window=3).mean()
                
                fig_trends = go.Figure()
                fig_trends.add_trace(go.Scatter(
                    x=video_stats.index,
                    y=video_stats['views'],
                    name="Views",
                    mode='lines+markers'
                ))
                fig_trends.add_trace(go.Scatter(
                    x=video_stats.index,
                    y=video_stats['ma_views'],
                    name="3-Video Moving Average",
                    line=dict(dash='dot')
                ))
                
                fig_trends.update_layout(
                    title="View Count Trends",
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x'
                )
                st.plotly_chart(fig_trends, use_container_width=True)
        
        # AI Insights
        st.markdown("<h2>🤖 Smart Insights</h2>", unsafe_allow_html=True)
        
        with st.container():
            try:
                insight_generator = AnalyticsInsightGenerator()
                insights = insight_generator.generate_insights(
                    channel_stats, 
                    video_stats, 
                    subscriber_stats
                )
                
                for insight in insights:
                    if insight.strip():
                        st.markdown(f'<div class="insight-box">{insight.strip()}</div>', 
                                  unsafe_allow_html=True)
                
            except Exception as e:
                st.error("Unable to generate insights at this time.")
        
        # Footer
        st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            Made with ❤️ by Your Team
        </div>
        """, unsafe_allow_html=True)
        
        # Export Data
        st.markdown("<h2>📥 Export Data</h2>", unsafe_allow_html=True)
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                try:
                    if not video_stats.empty:
                        csv = video_stats.to_csv(index=False)
                        st.download_button(
                            "📥 Export Video Stats",
                            csv,
                            "video_stats.csv",
                            "text/csv",
                            key='video-stats-download'
                        )
                    else:
                        st.info("No video statistics available to export.")
                except Exception as e:
                    st.error("Error preparing video stats export.")
            
            with col2:
                try:
                    if not subscriber_stats.empty:
                        csv = subscriber_stats.to_csv(index=False)
                        st.download_button(
                            "📥 Export Subscriber Stats",
                            csv,
                            "subscriber_stats.csv",
                            "text/csv",
                            key='subscriber-stats-download'
                        )
                    else:
                        st.info("No subscriber statistics available to export.")
                except Exception as e:
                    st.error("Error preparing subscriber stats export.")
        
    except Exception as e:
        st.error("⚠️ Application Error")
        st.info("Please verify your YouTube API credentials and permissions.")

if __name__ == "__main__":
    main() 