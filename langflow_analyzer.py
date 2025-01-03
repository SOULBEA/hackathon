import pandas as pd
import streamlit as st

class AnalyticsInsightGenerator:
    def __init__(self):
        pass

    def generate_insights(self, channel_stats, video_stats, subscriber_stats):
        insights = []
        
        try:
            # Channel growth insights
            total_views = int(channel_stats['viewCount'])
            total_subs = int(channel_stats['subscriberCount'])
            total_videos = int(channel_stats['videoCount'])
            
            avg_views_per_video = total_views / total_videos if total_videos > 0 else 0
            
            insights.append(f"📈 Channel averages {int(avg_views_per_video):,} views per video")
            insights.append(f"👥 Growing community of {total_subs:,} subscribers")
            
            # Video performance insights
            if not video_stats.empty:
                max_views = video_stats['views'].max()
                avg_views = video_stats['views'].mean()
                if avg_views > 0:
                    top_performance = (max_views - avg_views) / avg_views * 100
                    insights.append(f"🔥 Top performing video outperforms average by {int(top_performance)}%")
                
                # Engagement analysis
                if 'likes' in video_stats.columns and 'comments' in video_stats.columns:
                    avg_engagement_rate = ((video_stats['likes'].mean() + video_stats['comments'].mean()) / video_stats['views'].mean()) * 100
                    insights.append(f"💫 Average engagement rate of {avg_engagement_rate:.1f}%")
            
            # Subscriber insights
            if not subscriber_stats.empty:
                total_gained = subscriber_stats['gained'].sum()
                total_lost = subscriber_stats['lost'].sum()
                net_growth = total_gained - total_lost
                if total_gained > 0:
                    retention_rate = ((total_gained - total_lost) / total_gained) * 100
                    insights.append(f"⭐ Subscriber retention rate of {retention_rate:.1f}%")
                    
                    # Growth trend
                    if net_growth > 0:
                        growth_rate = (net_growth / total_subs) * 100
                        insights.append(f"📱 Channel growing at {growth_rate:.1f}% rate")
            
        except Exception as e:
            insights.append("📊 Analyzing your channel metrics...")
            
        return insights 