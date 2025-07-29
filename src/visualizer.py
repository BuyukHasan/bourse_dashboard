import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

class Visualizer:
    def __init__(self, data_frame, rows=2, columns=2, row_heights=None):
        """
        Initialise le visualiseur avec une grille de subplots.
        
        Args:
            data_frame (pd.DataFrame): DataFrame contenant les données
            rows (int): Nombre de lignes de subplots
            columns (int): Nombre de colonnes de subplots
            row_heights (list): Liste des hauteurs relatives des lignes
        """
        self.df = data_frame
        self.max_row = rows
        self.max_column = columns
        self.current_row = 1
        self.current_col = 1
        self.last_row = 1  # Dernière position utilisée
        self.last_col = 1  # Dernière position utilisée
        self.occupied_positions = set()
        
        if row_heights is None:
            row_heights = [1.0/rows] * rows
        
        self.fig = make_subplots(
            rows=rows, 
            cols=columns,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=row_heights
        )
    def reset_position(self):
        """Réinitialise le pointeur à la position (1,1)"""
        self.current_row = 1
        self.current_col = 1
        self.last_row = 1
        self.last_col = 1
        self.occupied_positions.clear()
        return self
    def _next_position(self):
        """Gère le positionnement automatique des graphiques."""
        current_pos = (self.current_row, self.current_col)
        self.occupied_positions.add(current_pos)
        
        if self.current_col < self.max_column:
            self.current_col += 1
        else:
            self.current_col = 1
            if self.current_row < self.max_row:
                self.current_row += 1
            else:
                print("Avertissement : Tous les emplacements sont occupés")
                self.current_row, self.current_col = 1, 1
        
        return current_pos
    
    def _add_trace(self, trace, overlay=False, row=None, col=None):
        """Méthode interne pour ajouter une trace."""
        if overlay:
            row, col = self.last_row, self.last_col  # Utilise la dernière position
        elif row is None or col is None:
            row, col = self._next_position()
        
        self.fig.add_trace(trace, row=row, col=col)
        self.last_row, self.last_col = row, col  # Mémorise la dernière position
        return self

    def _check_columns(self, required_columns):
        """Vérifie les colonnes nécessaires pour une méthode spécifique."""
        missing = [col for col in required_columns if col not in self.df.columns]
        if missing:
            raise ValueError(f"Colonnes manquantes: {missing}")

    def MA_draw(self, overlay=False):
        """Affiche les prix et moyennes mobiles."""
        self._check_columns(['MA_200', 'MA_50', 'Clôt'])
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']
        
        traces = [
            go.Scatter(x=dates, y=self.df['Clôt'], name='Prix (Clôt)', line=dict(color='blue')),
            go.Scatter(x=dates, y=self.df['MA_50'], name='MA 50', line=dict(color='orange', dash='dot')),
            go.Scatter(x=dates, y=self.df['MA_200'], name='MA 200', line=dict(color='red', dash='dash'))
        ]
        
        for trace in traces:
            self._add_trace(trace, overlay=overlay)
        return self

    def Rsi_draw(self, show_zones=True, overlay=False):
        """Affiche l'indicateur RSI."""
        self._check_columns(['rsi'])
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']
        
        self._add_trace(
            go.Scatter(
                x=dates, y=self.df['rsi'], name='RSI',
                line=dict(color='black', dash='dash')
            ),
            overlay=overlay
        )
        
        if show_zones:
            self._add_trace(
                go.Scatter(
                    x=dates, y=[70]*len(dates), fill='tonexty',
                    mode='none', fillcolor='rgba(255,0,0,0.2)',
                    showlegend=False, hoverinfo="skip"
                ),
                overlay=True
            )
            self._add_trace(
                go.Scatter(
                    x=dates, y=[30]*len(dates), fill='tozeroy',
                    mode='none', fillcolor='rgba(0,255,0,0.2)',
                    showlegend=False, hoverinfo="skip"
                ),
                overlay=True
            )
        return self

    def draw_candlestick(self, overlay=False, increasing_color='green', decreasing_color='red'):
        """Ajoute un graphique de chandeliers."""
        self._check_columns(['Ouv', 'Haut', 'Bas', 'Clôt'])
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']
    
        self._add_trace(
            go.Candlestick(
                x=dates,
                open=self.df['Ouv'],
                high=self.df['Haut'],
                low=self.df['Bas'],
                close=self.df['Clôt'],
                name='Chandeliers',
                increasing=dict(line=dict(color=increasing_color)),
                decreasing=dict(line=dict(color=decreasing_color))
            ),
            overlay=overlay
        )
        return self

    def draw_volume(self, overlay=False, color='blue'):
        """Affiche les volumes échangés."""
        self._check_columns(['Volume'])
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']
    
        self._add_trace(
            go.Bar(
                x=dates, y=self.df['Volume'], name='Volume',
                marker_color=color, opacity=0.7
            ),
            overlay=overlay
        )
        return self

    def draw_cumulative_returns(self, overlay=False, color='blue'):
        """Affiche les rendements cumulés."""
        self._check_columns(['rendements'])
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']
        cumulative_returns = (1 + self.df['rendements']).cumprod() - 1
        
        self._add_trace(
            go.Scatter(
                x=dates, y=cumulative_returns,
                name='Rendements cumulés',
                line=dict(color=color, width=2),
                mode='lines'
            ),
            overlay=overlay
        )
        return self

    def show(self, log_scale=False):
        """Affiche le graphique final."""
        self.fig.update_layout(
            hovermode='x unified',
            xaxis_rangeslider_visible=False,
            height=600,
            margin=dict(l=50, r=50, b=50, t=50)
        )
        
        if log_scale:
            self.fig.update_yaxes(type="log")
            
        self.fig.show()
        return self