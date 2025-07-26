import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
class Visualizer :

    def __init__(self,data_frame) :
        # Vérification des colonnes nécessaires
        required_columns = ['MA_200', 'MA_50', 'Clôt']
        if not all(col in data_frame.columns for col in required_columns):
            raise ValueError("Il manque des colonnes nécessaires")
        self.df = data_frame
        self.fig = make_subplots(
            rows=2, cols=1,  # 2 lignes, 1 colonne
            shared_xaxes=True,  # Partage l'axe X
            vertical_spacing=0.05,  # Espace entre les graphiques
            row_heights=[0.7, 0.3]  # 70% pour le prix, 30% pour le RSI
        )
    def MA_draw(self):
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
        ) ,row = 1 , col =1)
    
        self.fig.add_trace(go.Scatter(
            x=dates,
            y=self.df['MA_50'],
            name='Moyenne 50 jours',
            line=dict(color='orange', dash='dot')
        ) ,row = 1 , col =1)
    
        self.fig.add_trace(go.Scatter(
            x=dates,
            y=self.df['MA_200'],
            name='Moyenne 200 jours',
            line=dict(color='red', dash='dash')
        ) , row = 1 , col =1)
        # Configuration des axes
        self.fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Price',
            hovermode='x unified'
            )
    def Rsi_draw(self) : 
        """Affiche les prix et moyennes mobiles avec les dates en X."""
        # Reset l'index pour convertir les dates en colonne si nécessaire
        if isinstance(self.df.index, pd.DatetimeIndex):
            dates = self.df.index
        else:
            dates = self.df['Date']  # Si vos dates sont dans une colonne
        self.fig.add_trace(
            go.Scatter(
                x = dates ,
                y = self.df['rsi'] ,
                name='RSI',
                line=dict(color='black', dash='dash')
            ) , row = 2 , col = 1
        )   
    def overpurchaseselling(self):
        """Ajoute les zones de sur-achat/sur-vente au graphique RSI."""
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']

        # Zone de sur-achat (RSI > 70)
        self.fig.add_trace(go.Scatter(
            x=dates,
            y=[70] * len(dates),  # Ligne horizontale à 70
            fill='tonexty',        # Remplissage jusqu'à l'axe X
            mode='none',
            fillcolor='rgba(255, 0, 0, 0.2)',
            name='Sur-achat (RSI > 70)',
            showlegend=False,      # Évite la duplication dans la légende
        ) , row=2, col=1)
    
        # Zone de sur-vente (RSI < 30)
        self.fig.add_trace(go.Scatter(
            x=dates,
            y=[30] * len(dates),  # Ligne horizontale à 30
            fill='tozeroy',        # Remplissage jusqu'à zéro
            mode='none',
            fillcolor='rgba(0, 255, 0, 0.2)',
            name='Sur-vente (RSI < 30)',
            showlegend=False,
        ) , row=2, col=1)
    def show_graph(self) :
        self.fig.show()