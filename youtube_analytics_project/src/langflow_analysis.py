# filepath: src/langflow_analysis.py
import langflow

def analyze_engagement(data):
    langflow_instance = langflow.Langflow()
    insights = langflow_instance.generate_insights(data)
    return insights