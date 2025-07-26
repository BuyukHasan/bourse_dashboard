import plotly.graph_objects as go
import pandas as pd

class Visualizer :

    def __init__(self,data_frame) :
        # Vérification des colonnes nécessaires
        required_columns = ['MA_200', 'MA_50', 'Clôt']
        if not all(col in data_frame.columns for col in required_columns):
            raise ValueError("Il manque des colonnes nécessaires")
        self.df = data_frame
        self.fig = go.Figure()
    def show_MA(self):
        """Affiche les prix et moyennes mobiles avec les dates en X."""
        # Reset l'index pour convertir les dates en colonne si nécessaire
        if isinstance(self.df.index, pd.DatetimeIndex):
            dates = self.df.index
        else:
            dates = self.df['Date']  # Si vos dates sont dans une colonne
    
        # Ajout des traces une par une
        self.fig.add_trace(go.Scatter(
            x=dates,
            y=self.df['Clôt'],
            name='Prix (Clôt)',
            line=dict(color='blue')
        ))
    
        self.fig.add_trace(go.Scatter(
            x=dates,
            y=self.df['MA_50'],
            name='Moyenne 50 jours',
            line=dict(color='orange', dash='dot')
        ))
    
        self.fig.add_trace(go.Scatter(
            x=dates,
            y=self.df['MA_200'],
            name='Moyenne 200 jours',
            line=dict(color='red', dash='dash')
        ))
        self.fig.show()