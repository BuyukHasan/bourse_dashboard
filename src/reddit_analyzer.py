import random

class RedditSentiment:
    """Class to analyze Reddit sentiment (simulated)"""
    
    def __init__(self):
        pass  # No authentication needed
    
    def analyze_ticker(self, ticker):
        """
        Simulated sentiment analysis without API access
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            dict: Simulated sentiment analysis results
        """
        return {
            'positive': random.randint(5, 15),
            'neutral': random.randint(20, 30),
            'negative': random.randint(5, 15),
            'total': 50,
            'sample': "Simulation without Reddit access"
        }