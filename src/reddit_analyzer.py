import random

class RedditSentiment:
    def __init__(self):
        pass  # No authentication needed
    
    def analyze_ticker(self, ticker):
        """Simulated version without API"""
        return {
            'positive': random.randint(5, 15),
            'neutral': random.randint(20, 30),
            'negative': random.randint(5, 15),
            'total': 50,
            'sample': "Simulation without Reddit access"
        }