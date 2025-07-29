import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

class Visualizer:
    def __init__(self, data_frame, rows=2, columns=2, row_heights=None):
        """
        Initializes the visualizer with a grid of subplots.

        Args:
            data_frame (pd.DataFrame): DataFrame containing the data
            rows (int): Number of subplot rows
            columns (int): Number of subplot columns
            row_heights (list): List of relative row heights
        """
        self.df = data_frame
        self.max_row = rows
        self.max_column = columns
        self.current_row = 1
        self.current_col = 1
        self.last_row = 1  # Last used position
        self.last_col = 1  # Last used position
        self.occupied_positions = set()
        
        if row_heights is None:
            row_heights = [1.0 / rows] * rows
        
        self.fig = make_subplots(
            rows=rows, 
            cols=columns,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=row_heights
        )

    def reset_position(self):
        """Resets the pointer to position (1,1)"""
        self.current_row = 1
        self.current_col = 1
        self.last_row = 1
        self.last_col = 1
        self.occupied_positions.clear()
        return self

    def _next_position(self):
        """Handles automatic subplot positioning."""
        current_pos = (self.current_row, self.current_col)
        self.occupied_positions.add(current_pos)
        
        if self.current_col < self.max_column:
            self.current_col += 1
        else:
            self.current_col = 1
            if self.current_row < self.max_row:
                self.current_row += 1
            else:
                print("Warning: All subplot positions are occupied.")
                self.current_row, self.current_col = 1, 1
        
        return current_pos
    
    def _add_trace(self, trace, overlay=False, row=None, col=None):
        """Internal method to add a trace to the plot."""
        if overlay:
            row, col = self.last_row, self.last_col  # Use last used position
        elif row is None or col is None:
            row, col = self._next_position()
        
        self.fig.add_trace(trace, row=row, col=col)
        self.last_row, self.last_col = row, col  # Save last used position
        return self

    def _check_columns(self, required_columns):
        """Checks that required columns are present in the DataFrame."""
        missing = [col for col in required_columns if col not in self.df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    def MA_draw(self, overlay=False):
        """Displays closing price and moving averages."""
        self._check_columns(['MA_200', 'MA_50', 'Clôt'])
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']
        
        traces = [
            go.Scatter(x=dates, y=self.df['Clôt'], name='Close Price', line=dict(color='blue')),
            go.Scatter(x=dates, y=self.df['MA_50'], name='MA 50', line=dict(color='orange', dash='dot')),
            go.Scatter(x=dates, y=self.df['MA_200'], name='MA 200', line=dict(color='red', dash='dash'))
        ]
        
        for trace in traces:
            self._add_trace(trace, overlay=overlay)
        return self

    def Rsi_draw(self, show_zones=True, overlay=False):
        """Displays the RSI indicator with optional threshold zones."""
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
                    x=dates, y=[70] * len(dates), fill='tonexty',
                    mode='none', fillcolor='rgba(255,0,0,0.2)',
                    showlegend=False, hoverinfo="skip"
                ),
                overlay=True
            )
            self._add_trace(
                go.Scatter(
                    x=dates, y=[30] * len(dates), fill='tozeroy',
                    mode='none', fillcolor='rgba(0,255,0,0.2)',
                    showlegend=False, hoverinfo="skip"
                ),
                overlay=True
            )
        return self

    def draw_candlestick(self, overlay=False, increasing_color='green', decreasing_color='red'):
        """Adds a candlestick chart to the figure."""
        self._check_columns(['Ouv', 'Haut', 'Bas', 'Clôt'])
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']
    
        self._add_trace(
            go.Candlestick(
                x=dates,
                open=self.df['Ouv'],
                high=self.df['Haut'],
                low=self.df['Bas'],
                close=self.df['Clôt'],
                name='Candlesticks',
                increasing=dict(line=dict(color=increasing_color)),
                decreasing=dict(line=dict(color=decreasing_color))
            ),
            overlay=overlay
        )
        return self

    def draw_volume(self, overlay=False, color='blue'):
        """Displays traded volume as a bar chart."""
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
        """Plots cumulative returns."""
        self._check_columns(['rendements'])
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']
        cumulative_returns = (1 + self.df['rendements']).cumprod() - 1
        
        self._add_trace(
            go.Scatter(
                x=dates, y=cumulative_returns,
                name='Cumulative Returns',
                line=dict(color=color, width=2),
                mode='lines'
            ),
            overlay=overlay
        )
        return self

    def show(self, log_scale=False):
        """Displays the final chart."""
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