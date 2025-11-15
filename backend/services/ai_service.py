import random

class AIService:
    @staticmethod
    def analyze_emotion(text, mood):
        """
        Analyze emotion from text and mood
        In production, integrate with actual AI/ML model
        """
        # Mock analysis based on mood
        mood_scores = {
            'very-happy': {'positive': 85, 'neutral': 10, 'negative': 5},
            'happy': {'positive': 70, 'neutral': 20, 'negative': 10},
            'neutral': {'positive': 40, 'neutral': 50, 'negative': 10},
            'sad': {'positive': 20, 'neutral': 30, 'negative': 50},
            'very-sad': {'positive': 10, 'neutral': 20, 'negative': 70},
            'angry': {'positive': 15, 'neutral': 25, 'negative': 60}
        }
        
        base_scores = mood_scores.get(mood, {'positive': 50, 'neutral': 30, 'negative': 20})
        
        # Add some randomness
        emotion_score = {
            'positive': base_scores['positive'] + random.randint(-10, 10),
            'neutral': base_scores['neutral'] + random.randint(-5, 5),
            'negative': base_scores['negative'] + random.randint(-5, 5)
        }
        
        # Calculate wellness score
        wellness_score = int(
            emotion_score['positive'] * 0.7 + 
            emotion_score['neutral'] * 0.2 - 
            emotion_score['negative'] * 0.1
        )
        
        # Generate suggestions
        suggestions = AIService._generate_suggestions(emotion_score)
        
        return {
            'emotionScore': emotion_score,
            'wellnessScore': max(0, min(100, wellness_score)),
            'suggestions': suggestions,
            'sentiment': AIService._determine_sentiment(emotion_score)
        }
    
    @staticmethod
    def _generate_suggestions(emotion_score):
        all_suggestions = {
            'positive': [
                '🎵 Hãy nghe một bản nhạc yêu thích để giữ vững tâm trạng tích cực',
                '📝 Viết ra 3 điều bạn biết ơn hôm nay',
                '🤝 Chia sẻ niềm vui với người thân',
            ],
            'neutral': [
                '🚶 Đi dạo 10-15 phút ngoài trời',
                '📖 Đọc một câu chuyện ngắn truyền cảm hứng',
                '🧘 Thử nghiệm bài tập thở sâu 5 phút',
            ],
            'negative': [
                '💭 Cho phép mình được cảm nhận cảm xúc, điều đó hoàn toàn bình thường',
                '🎧 Nghe podcast hoặc nhạc thư giãn',
                '💬 Nói chuyện với người bạn tin tưởng',
                '✍️ Viết ra những suy nghĩ để giải tỏa',
            ]
        }
        
        if emotion_score['positive'] > 60:
            return random.sample(all_suggestions['positive'], 2)
        elif emotion_score['negative'] > 40:
            return random.sample(all_suggestions['negative'], 3)
        else:
            return random.sample(all_suggestions['neutral'], 2)
    
    @staticmethod
    def _determine_sentiment(emotion_score):
        if emotion_score['positive'] > 60:
            return 'positive'
        elif emotion_score['negative'] > 40:
            return 'negative'
        else:
            return 'neutral'