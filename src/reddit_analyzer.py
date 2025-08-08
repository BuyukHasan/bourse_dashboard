import random

class RedditSentiment:
    def __init__(self):
        pass  # Plus besoin d'authentification
    
    def analyze_ticker(self, ticker):
        """Version simulée sans API"""
        return {
            'positive': random.randint(5, 15),
            'neutral': random.randint(20, 30),
            'negative': random.randint(5, 15),
            'total': 50,
            'sample': "Simulation sans accès Reddit"
        }
    