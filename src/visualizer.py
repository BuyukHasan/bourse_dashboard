import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from src.technical_analyzer import TechnicalAnalyzer
from plotly.subplots import make_subplots

class Visualizer:
    def __init__(self, data_frame, rows=2, columns=2, row_heights=None):
        """
        Initialize visualizer with subplot grid
        Args:
            data_frame (pd.DataFrame): Input data
            rows (int): Number of rows
            columns (int): Number of columns
            row_heights (list): Relative row heights
        """
        self.df = data_frame
        self.max_row = rows
        self.max_column = columns
        self.current_row = 1
        self.current_col = 1
        self.last_row = 1
        self.last_col = 1
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
        """Reset pointer to position (1,1)"""
        self.current_row = 1
        self.current_col = 1
        self.last_row = 1
        self.last_col = 1
        self.occupied_positions.clear()
        return self

    def _next_position(self):
        """Handle automatic subplot positioning"""
        current_pos = (self.current_row, self.current_col)
        self.occupied_positions.add(current_pos)
        
        if self.current_col < self.max_column:
            self.current_col += 1
        else:
            self.current_col = 1
            if self.current_row < self.max_row:
                self.current_row += 1
            else:
                print("Warning: All subplot positions occupied")
                self.current_row, self.current_col = 1, 1
        
        return current_pos
    
    def _add_trace(self, trace, overlay=False, row=None, col=None):
        """Internal method to add trace"""
        if overlay:
            row, col = self.last_row, self.last_col
        elif row is None or col is None:
            row, col = self._next_position()
        
        self.fig.add_trace(trace, row=row, col=col)
        self.last_row, self.last_col = row, col
        return self

    def _check_columns(self, required_columns):
        """Check required columns exist"""
        missing = [col for col in required_columns if col not in self.df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    def MA_draw(self, overlay=False):
        """Display closing price and moving averages"""
        self._check_columns(['MA_200', 'MA_50', 'Close'])
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']
        
        traces = [
            go.Scatter(x=dates, y=self.df['Close'], name='Close Price', line=dict(color='blue')),
            go.Scatter(x=dates, y=self.df['MA_50'], name='MA 50', line=dict(color='orange', dash='dot')),
            go.Scatter(x=dates, y=self.df['MA_200'], name='MA 200', line=dict(color='red', dash='dash'))
        ]
        
        for trace in traces:
            self._add_trace(trace, overlay=overlay)
        return self

    def Rsi_draw(self, show_zones=True, overlay=False):
        """Display RSI indicator with threshold zones"""
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
        """Add candlestick chart"""
        self._check_columns(['Open', 'High', 'Low', 'Close'])
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']
    
        self._add_trace(
            go.Candlestick(
                x=dates,
                open=self.df['Open'],
                high=self.df['High'],
                low=self.df['Low'],
                close=self.df['Close'],
                name='Candlesticks',
                increasing=dict(line=dict(color=increasing_color)),
                decreasing=dict(line=dict(color=decreasing_color))
            ),
            overlay=overlay
        )
        return self

    def draw_volume(self, overlay=False, color='blue'):
        """Display traded volume"""
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
        """Plot cumulative returns"""
        self._check_columns(['returns'])
        dates = self.df.index if isinstance(self.df.index, pd.DatetimeIndex) else self.df['Date']
        cumulative_returns = (1 + self.df['returns']).cumprod() - 1
        
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

    def draw_multiple_tickers(self, tickers_data, overlay=False, colors=None):
        """
        Display multiple price series
        Args:
            tickers_data (dict): {ticker: DataFrame}
            overlay (bool): Overlay on current plot
            colors (list): Color list for each series
        """
        if not isinstance(tickers_data, dict):
            raise ValueError("tickers_data must be a {ticker: df} dictionary")
    
        if not colors:
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
        for i, (ticker, df) in enumerate(tickers_data.items()):
            if 'Close' not in df.columns:
                raise ValueError(f"DataFrame for {ticker} missing 'Close' column")
        
            self._add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['Close'],
                    name=ticker,
                    line=dict(color=colors[i % len(colors)], width=2),
                    mode='lines'
                ),
                overlay=overlay
            )
        return self

    def show(self, log_scale=False, title=None):
        """Display final chart with improved style"""
        self.fig.update_layout(
            template="plotly_white",
            hovermode='x unified',
            xaxis_rangeslider_visible=False,
            height=600,
            margin=dict(l=50, r=50, b=50, t=50 if title else 30),
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                font=dict(size=20)
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='rgba(240,240,240,0.8)',
            paper_bgcolor='rgba(240,240,240,0.1)'
        )
    
        if log_scale:
            self.fig.update_yaxes(type="log")
        
        self.fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='LightGrey')
        self.fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='LightGrey')
    
        st.plotly_chart(self.fig, use_container_width=True)
        return self
    
    @classmethod
    def test_visualizer(cls, df=None):
        """
        Generate visual test report
        Example:
        >>> analyzer = TechnicalAnalyzer.test_analyzer()
        >>> Visualizer.test_visualizer(analyzer.df)
        """
        if df is None:
            df = TechnicalAnalyzer.test_analyzer().df
    
        viz = cls(df, rows=2, cols=1)
        (viz.draw_candlestick(row=1, col=1)
        .draw_volume(row=2, col=1)
        .show())