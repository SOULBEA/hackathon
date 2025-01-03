import streamlit as st

class ChannelAdvisor:
    def __init__(self, channel_stats=None, video_stats=None, subscriber_stats=None):
        # Make stats optional since we'll use predefined responses
        self.responses = {
            "greeting": [
                "Hello! I'm your YouTube Channel Advisor. I can help you with:",
                "• Channel growth strategies",
                "• Content optimization",
                "• Audience engagement",
                "• SEO tips",
                "• Best practices",
                "\nWhat would you like to know about?"
            ],
            
            "growth": [
                "Here are some proven strategies for channel growth:",
                "1. 📈 Maintain a consistent upload schedule (2-3 times per week)",
                "2. 🎯 Focus on a specific niche to build a loyal audience",
                "3. 🔍 Use YouTube SEO best practices",
                "4. 📱 Promote your content on other social platforms",
                "5. 🤝 Engage with your community regularly",
                "\nWould you like more specific details about any of these points?"
            ],
            
            "content": [
                "Here's how to create engaging content:",
                "1. 📊 Plan content series or playlists",
                "2. 🎬 Hook viewers in the first 15 seconds",
                "3. 🎯 Create compelling thumbnails and titles",
                "4. 📝 Add value in every video",
                "5. 💡 Include clear calls-to-action",
                "\nWhich aspect would you like me to elaborate on?"
            ],
            
            "seo": [
                "Let me help you with YouTube SEO:",
                "1. 🔍 Research trending keywords in your niche",
                "2. 📝 Optimize titles, descriptions, and tags",
                "3. 🎨 Create clickable thumbnails",
                "4. 📊 Use YouTube Analytics to track performance",
                "5. 🏷️ Add relevant tags and chapters",
                "\nNeed more specific SEO tips?"
            ]
        }

    def get_growth_suggestions(self, user_input):
        input_lower = user_input.lower()
        
        # Handle greetings
        if any(word in input_lower for word in ['hi', 'hello', 'hey']):
            return self._format_response(self.responses["greeting"])
        
        # Handle growth questions
        if any(word in input_lower for word in ['grow', 'increase', 'improve']):
            return self._format_response([
                "Let's help your channel grow! 🚀",
                "",
                *self.responses["growth"][1:],
                "",
                "I can provide more specific advice about:",
                "• Content strategy",
                "• SEO optimization",
                "• Audience engagement",
                "• Best practices",
                "Just ask!"
            ])
        
        # Handle content questions
        if any(word in input_lower for word in ['content', 'video', 'make']):
            return self._format_response([
                "Here's how to create better content! 🎥",
                "",
                *self.responses["content"][1:],
                "",
                "Want to know more about any specific point?"
            ])
        
        # Handle SEO questions
        if any(word in input_lower for word in ['seo', 'rank', 'search']):
            return self._format_response([
                "Let's optimize your channel for search! 🔍",
                "",
                *self.responses["seo"][1:],
                "",
                "I can provide more detailed SEO strategies if needed."
            ])
        
        # Handle engagement questions
        if any(word in input_lower for word in ['engage', 'community', 'comment']):
            return self._format_response([
                "Here's how to boost engagement! 🤝",
                "",
                "1. Respond to comments quickly",
                "2. Ask questions in your videos",
                "3. Create community posts",
                "4. Host live streams",
                "5. Run polls and surveys",
                "",
                "Which engagement strategy interests you most?"
            ])
        
        # Default response
        return self._format_response([
            "I can help you with various aspects of YouTube success! 📱",
            "",
            "Try asking about:",
            "• Channel growth strategies",
            "• Content creation tips",
            "• SEO optimization",
            "• Audience engagement",
            "• Best practices",
            "",
            "What would you like to learn more about?"
        ])

    def _format_response(self, response_list):
        return "\n".join(response_list) 