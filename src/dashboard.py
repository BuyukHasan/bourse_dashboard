import streamlit as st
from src.technical_analyzer import TechnicalAnalyzer
from datetime import datetime
from src.data_fetcher import DataFetcher
from src.visualizer import Visualizer
from src.news_fetcher import NewsFetcher
from src.reddit_analyzer import RedditSentiment

class Dashboard:
    def __init__(self, data_frame):
        self.tickers = ["AAPL", "TSLA", "MSFT", "AMZN", "GOOGL"]
        self.default_start_date = datetime.now().replace(year=datetime.now().year-1)
        self.df = data_frame
        
    def _set_global_style(self):
        """Configure global dashboard style"""
        primary_color = "#2c3e50"
        secondary_color = "#3498db"
        background_color = "#f8f9fa"
    
        st.set_page_config(
            page_title="Stock Market Dashboard",
            layout="wide",
            page_icon="📊"
        )
    
        st.markdown(f"""
        <style>
            .css-18e3th9 {{
                background-color: {background_color};
            }}
            .css-1d391kg {{
                background-color: {primary_color};
                color: white;
            }}
            .stMetric {{
                border-left: 0.25rem solid {secondary_color};
                padding: 1rem;
                border-radius: 0.5rem;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .stTabs [data-baseweb="tab-list"] {{
                gap: 0.5rem;
            }}
            .stTabs [data-baseweb="tab"] {{
                padding: 0.5rem 1rem;
                border-radius: 0.5rem 0.5rem 0 0;
            }}
            .stTabs [aria-selected="true"] {{
                background-color: {secondary_color};
                color: white;
            }}
            .css-1vq4p4l {{
                padding: 2rem 1rem;
                background-color: {primary_color};
                color: white;
            }}
            .sidebar .sidebar-content {{
                background-color: {primary_color};
            }}
        </style>
        """, unsafe_allow_html=True)
        
    def _create_sidebar_controls(self):
        self.selected_ticker = st.sidebar.selectbox(
            "Select a stock:", 
            self.tickers,
            key="unique_ticker_select"
        )
        self.start_date = st.sidebar.date_input(
            "Start date:", 
            value=self.default_start_date,
            key="unique_start_date"
        )
        self.end_date = st.sidebar.date_input(
            "End date:", 
            value=datetime.now(),
            key="unique_end_date"
        )
        
        if st.sidebar.button("Apply changes"):
            self._reload_data()
    
    def _reload_data(self):
        """Load data with progress indicator"""
        with st.spinner(f"Loading data for {self.selected_ticker}..."):
            progress_bar = st.progress(0)
        
            try:
                fetcher = DataFetcher(self.selected_ticker)
                progress_bar.progress(20)
            
                new_df = fetcher.fetch_data(start=self.start_date, end=self.end_date)
                progress_bar.progress(50)
            
                if not new_df.empty:
                    analyzer = TechnicalAnalyzer(new_df)
                    analyzer.compute_50_200_days()
                    progress_bar.progress(70)
                    analyzer.add_rsi()
                    analyzer.calculate_volatility()
                    # Generate required columns for returns
                    analyzer.add_signal_column()
                    analyzer.add_performance_column()
                    analyzer.add_returns_columns()
                    progress_bar.progress(90)
                
                    self.df = analyzer.df
                    st.session_state.df = analyzer.df
                    progress_bar.progress(100)
                
                    st.toast("Data updated successfully!", icon="✅")
                    st.rerun()
                else:
                    st.sidebar.error("No data available for these parameters")
            except Exception as e:
                st.sidebar.error(f"Error loading data: {str(e)}")
            finally:
                progress_bar.empty()
    
    def _display_kpis(self):
        """Display key indicators with improved style"""
        cols = st.columns(4)
    
        price_change = self.df['Close'].pct_change().iloc[-1] * 100
        cols[0].metric(
            label="💰 Current Price",
            value=f"{self.df['Close'].iloc[-1]:.2f} $",
            delta=f"{price_change:.2f}%",
            delta_color="normal",
            help="Last closing price with daily variation"
        )
    
        volatility = self.df['Volatility'].iloc[-1] * 100
        volatility_icon = "📈" if volatility < 5 else "📉" if volatility > 15 else "📊"
        cols[1].metric(
            label=f"{volatility_icon} Volatility (30d)",
            value=f"{volatility:.1f}%",
            help="Annualized 30-day volatility"
        )
    
        volume = self.df['Volume'].iloc[-1]
        cols[2].metric(
            label="📦 Daily Volume",
            value=f"{volume/1e6:.1f}M",
            help="Traded volume in millions"
        )
    
        if 'rsi' in self.df.columns:
            rsi_value = self.df['rsi'].iloc[-1]
            rsi_status = "Buy" if rsi_value < 30 else "Sell" if rsi_value > 70 else "Neutral"
            cols[3].metric(
                label=f"📊 RSI (14d) - {rsi_status}",
                value=f"{rsi_value:.1f}",
                help="Relative Strength Index - <30: Oversold, >70: Overbought"
            )

    def _create_analysis_tabs(self):
        """Create analysis tabs with enriched content"""
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Main Chart", 
            "📊 Technical Analysis", 
            "🔍 Raw Data",
            "📰 News & Sentiment"
        ])

        with tab1:
            st.markdown("#### Price evolution with moving averages")
            fig = Visualizer(self.df, rows=1, columns=1)
            fig.draw_candlestick().MA_draw(overlay=True)
            fig.show(title=f"Analysis of {self.selected_ticker}")
        
            st.markdown("##### Recent trends")
            col1, col2 = st.columns(2)
            with col1:
                last_5_days = self.df['Close'].pct_change(5).iloc[-1] * 100
                st.metric("Last 5 days", f"{last_5_days:.2f}%")
            with col2:
                last_month = self.df['Close'].pct_change(20).iloc[-1] * 100
                st.metric("1 month", f"{last_month:.2f}%")

        with tab2:
            st.markdown("#### Complete technical analysis")
            cols = st.columns(2)
        
            with cols[0]:
                st.markdown("##### Key indicators")
                fig1 = Visualizer(self.df, rows=2, columns=1, row_heights=[0.7, 0.3])
                fig1.draw_candlestick().Rsi_draw(show_zones=True)
                fig1.show()
            
            with cols[1]:
                st.markdown("##### Volume and volatility")
                fig2 = Visualizer(self.df, rows=2, columns=1, row_heights=[0.5, 0.5])
                fig2.draw_volume().draw_cumulative_returns()
                fig2.show()

        with tab3:
            st.markdown("#### Historical data")
            st.data_editor(
                self.df.sort_index(ascending=False),
                column_config={
                    "Open": st.column_config.NumberColumn(format="$%.2f"),
                    "High": st.column_config.NumberColumn(format="$%.2f"),
                    "Low": st.column_config.NumberColumn(format="$%.2f"),
                    "Close": st.column_config.NumberColumn(format="$%.2f"),
                    "Volume": st.column_config.NumberColumn(format="%.0f"),
                    "rsi": st.column_config.NumberColumn(format="%.1f"),
                    "Volatility": st.column_config.NumberColumn(format="%.2%")
                },
                hide_index=False,
                use_container_width=True,
                height=600
            )
        
        with tab4:
            self._display_news_analysis()
            
    def _display_news_analysis(self):
        """Display news and sentiment analysis"""
        st.subheader("📰 News and Sentiment Analysis")
    
        news = NewsFetcher().get_company_news(self.selected_ticker)
        reddit_data = RedditSentiment().analyze_ticker(self.selected_ticker)
    
        news_scores = [item['score'] for item in news]
        avg_news_score = sum(news_scores) / len(news_scores) if news_scores else 0
    
        reddit_score = (reddit_data['positive'] - reddit_data['negative']) / reddit_data['total']
    
        global_score = (avg_news_score + reddit_score) / 2
        
        st.markdown("### Investment Recommendation")
        if global_score > 0.3:
            st.success("✅ **Favorable to buy** - Very positive sentiment")
        elif global_score > -0.2:
            st.info("🟢 **Moderate opportunity** - Generally neutral sentiment")
        else:
            st.warning("⚠️ **Caution** - Dominant negative sentiment")
        
        st.metric("Confidence Score", f"{global_score:.2f}/1.0")
        
        st.markdown("### Latest News")
        for item in news:
            sentiment_color = {
                "positive": "green",
                "neutral": "orange",
                "negative": "red"
            }.get(item['sentiment'], "gray")
            
            st.markdown(f"""
            <div style="border-left: 3px solid {sentiment_color}; padding-left: 10px; margin-bottom: 15px;">
                <b>{item['title']}</b><br>
                <i>{item['source']} - {item['date']}</i><br>
                Sentiment: <span style="color: {sentiment_color}; font-weight: bold">{item['sentiment']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Social Media Sentiment")
        st.progress((reddit_data['positive'] / reddit_data['total']))
        st.caption(f"Positive: {reddit_data['positive']} | Neutral: {reddit_data['neutral']} | Negative: {reddit_data['negative']}")
        
    def _add_data_download(self):
        csv_data = self.df.to_csv(index=False).encode('utf-8')
        today = datetime.now().strftime("%Y-%m-%d")
        st.download_button(
            label="📥 Download data",
            data=csv_data,
            file_name=f'stock_data_{today}.csv',
            mime='text/csv',
            key=f"download_btn_{datetime.now().timestamp()}"
        )

    def display(self):
        """Version with alert system"""
        self._set_global_style()
    
        container = st.container()
        with container:
            self._create_sidebar_controls()
            self._create_alert_system()
    
            if hasattr(self, 'df'):
                self._check_alerts()
                self._display_kpis()
                self._create_analysis_tabs()
                self._add_data_download()
                
    def _create_alert_system(self):
        """Visually improved alert system"""
        with st.sidebar.expander("🔔 Alert System", expanded=True):
            if 'alerts' not in st.session_state:
                st.session_state.alerts = []
        
            with st.form("alert_form", clear_on_submit=True):
                cols = st.columns(2)
                with cols[0]:
                    indicator = st.selectbox(
                        "Indicator",
                        ["RSI", "Closing Price", "Volatility", "MA Crossover"],
                        key="alert_indicator"
                    )
                    condition = st.selectbox(
                        "Condition",
                        ["Above", "Below", "Crosses above", "Crosses below"],
                        key="alert_condition"
                    )
            
                with cols[1]:
                    threshold = st.number_input(
                        "Threshold",
                        min_value=0.0,
                        max_value=1000.0 if indicator == "Closing Price" else 100.0,
                        value=30.0 if indicator == "RSI" else 50.0,
                        step=0.1,
                        key="alert_threshold"
                    )
                    color = st.color_picker(
                        "Alert color",
                        value="#FF4B4B",
                        key="alert_color"
                    )
            
                if st.form_submit_button("➕ Add alert", use_container_width=True):
                    new_alert = {
                        'indicator': indicator,
                        'condition': condition,
                        'threshold': threshold,
                        'color': color,
                        'active': True,
                        'triggered': False
                    }
                    st.session_state.alerts.append(new_alert)
                    st.success("Alert saved!")
        
            if st.session_state.alerts:
                st.markdown("---")
                st.markdown("**My Active Alerts**")
            
                for i, alert in enumerate(st.session_state.alerts[:5]):
                    with st.container(border=True):
                        cols = st.columns([1, 3, 1])
                        with cols[0]:
                            st.checkbox(
                                "Active",
                                value=alert['active'],
                                key=f"alert_active_{i}",
                                on_change=lambda i=i: self._toggle_alert(i),
                                label_visibility="collapsed"
                            )
                        with cols[1]:
                            st.markdown(f"""
                            **{alert['indicator']}** {alert['condition']} **{alert['threshold']}**
                            """)
                        with cols[2]:
                            st.button(
                                "🗑️", 
                                key=f"delete_{i}",
                                on_click=lambda i=i: self._remove_alert(i),
                                use_container_width=True
                            )
                            
    def _toggle_alert(self, index):
        """Enable/disable an alert"""
        st.session_state.alerts[index]['active'] = not st.session_state.alerts[index]['active']

    def _remove_alert(self, index):
        """Remove an alert"""
        st.session_state.alerts.pop(index)
        st.rerun()

    def _check_alerts(self):
        """Check if alert conditions are met"""
        if not hasattr(self, 'df') or 'alerts' not in st.session_state:
            return
    
        for i, alert in enumerate(st.session_state.alerts):
            if not alert['active']:
                continue
            
            try:
                current_value = None
                message = ""
            
                if alert['indicator'] == "RSI":
                    current_value = self.df['rsi'].iloc[-1]
                elif alert['indicator'] == "Closing Price":
                    current_value = self.df['Close'].iloc[-1]
                elif alert['indicator'] == "Volatility":
                    current_value = self.df['Volatility'].iloc[-1] * 100
            
                if current_value is not None:
                    if alert['condition'] == "Above" and current_value > alert['threshold']:
                        message = f"🚨 {alert['indicator']} ({current_value:.2f}) > {alert['threshold']}"
                    elif alert['condition'] == "Below" and current_value < alert['threshold']:
                        message = f"🚨 {alert['indicator']} ({current_value:.2f}) < {alert['threshold']}"
                
                    elif alert['indicator'] == "MA Crossover":
                        if alert['condition'] == "Crosses above" and \
                            self.df['MA_50'].iloc[-1] > self.df['MA_200'].iloc[-1] and \
                            self.df['MA_50'].iloc[-2] <= self.df['MA_200'].iloc[-2]:
                            message = "🚨 Bullish crossover (MA50 > MA200)"
                        elif alert['condition'] == "Crosses below" and \
                            self.df['MA_50'].iloc[-1] < self.df['MA_200'].iloc[-1] and \
                            self.df['MA_50'].iloc[-2] >= self.df['MA_200'].iloc[-2]:
                            message = "🚨 Bearish crossover (MA50 < MA200)"
            
                    if message and not alert['triggered']:
                        st.toast(message, icon="🔔")
                        st.session_state.alerts[i]['triggered'] = True
                    elif not message and alert['triggered']:
                        st.session_state.alerts[i]['triggered'] = False
                    
            except KeyError as e:
                st.error(f"Error: Column {str(e)} missing for alert")
                
    @classmethod
    def test_dashboard(cls):
        """Launch a dashboard demo"""
        df = DataFetcher("TSLA").fetch_data(period="6mo")
        analyzer = TechnicalAnalyzer(df)
        analyzer.compute_50_200_days()
    
        dashboard = cls(analyzer.df)
        dashboard.display()